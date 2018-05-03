#-*- coding:utf-8 -*-
from app.extensions import mongo
from app.util import bson_obj_id, bson_to_json
from datetime import datetime
from flask import current_app
from flask.ext.login import UserMixin, current_user
from random import randint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

import json
import pymongo

class User(UserMixin):
    def __init__(self, user_id, extras=None):
        self.id = user_id
        if (extras is not None) and isinstance(extras, dict):
            for name, attr in extras.items():
                setattr(self, name, attr)

    @property
    def is_admin(self):
        return mongo.db['users'].find_one(
            {'_id': bson_obj_id(self.id), 'admin':True},
        ) != None

    def add_create(self):
        mongo.db['users'].update(
            {'_id': bson_obj_id(self.id)},
            {'$inc': {'create_count': 1}}
        )

    def add_edit(self):
        mongo.db['users'].update(
            {'_id': bson_obj_id(self.id)},
            {'$inc': {'edit_count': 1}}
        )

    @staticmethod
    def gen_passwd_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_passwd(passwd_hash, passwd):
        return check_password_hash(passwd_hash, passwd)

    def gen_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps(bson_to_json({"id": self.id}))

    @staticmethod
    def verify_auth_token(token):
        from app.extensions import mongo
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        dict_ = json.loads(data)
        return mongo.db.users.find_one({"_id": bson_obj_id(dict_['id']["$oid"])})

    @staticmethod
    def set_active(user_id):
        return mongo.db['users'].update(
            {'_id': user_id},
            {'$set':
                 {
                     'active': True
                 }
            }
        )

    @staticmethod
    def find_by_username(uname):
        return mongo.db.users.find_one({'username': uname})

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email':email})

    @staticmethod
    def find_by_id(id):
        return mongo.db.users.find_one({'_id': id})

    @classmethod
    def add_user(cls, email, username, password):
        return mongo.db['users'].insert({
            'email':email,
            'username':username,
            'password': cls.gen_passwd_hash(password),
            'avatar': '',
            'active': False,
            'join': datetime.utcnow(),
            'create_count':0,
            'edit_count':0
        })

    @classmethod
    def update_user(cls, id, data):
        mongo.db['users'].update(
            {'_id': id },
            {
                "$set": data
            }
        )

class ItemMixin(object):
    # Item CURD Mixin
    @staticmethod
    def _find_many(query):
        return mongo.db['items'].find(query)

    @staticmethod
    def _find_one(query):
        return mongo.db['items'].find_one(query)

    @staticmethod
    def _create_item(title, type):
        return mongo.db['items'].insert({
            'title': title,
            'type': type,
            'attributes':[],
            'attr_count': 1,
            'view': 0,
            'created_at': datetime.utcnow(),
            'created_by': current_user.id
        })

    @staticmethod
    def _del_item(query):
        return mongo.db['items'].remove(query)

    @staticmethod
    def _add_attr(query, attr_name, attr_value, attr_type):
        return mongo.db['items'].update(
            query,
            {
                '$inc': {'attr_count': 1},
                '$push':
                    {
                        'attributes':
                            {
                                'attr_name': attr_name,
                                'attr_value': attr_value,
                                'attr_type': attr_type
                            }
                    }
            }
        )

    @staticmethod
    def _edit_attr(query, attr_name, attr_value, attr_type):

        return mongo.db['items'].update(
            query,
            {
                '$set':
                    {
                        'attributes.$':
                            {
                                'attr_name': attr_name,
                                'attr_value': attr_value,
                                'attr_type': attr_type
                            }
                    }
            }
        )

    @staticmethod
    def _del_attr(query, attr_name):
        return mongo.db['items'].update(
                query,
                {
                    '$pull':
                    {
                        'attributes': {'attr_name': attr_name}
                    }
                }
            )

class Item(ItemMixin):
    @staticmethod
    def add_type(type_name):
        return mongo.db['types'].replace_one({'name': type_name},
                                 {'name': type_name, 'modified':datetime.utcnow()}, upsert=True )

    @staticmethod
    def del_type(type_name):
        return mongo.db['types'].remove({'name': type_name})

    @staticmethod
    def types():
        return mongo.db['types'].find()

    @staticmethod
    def add_param(dic, key, value):
        dic["attributes."+key] = value.strip()

    @staticmethod
    def get_random_item():
        N = mongo.db['items'].count()
        try:
            item = mongo.db['items'].find().limit(1).skip(randint(0, N-1))[0]
        except:
            item = None
        return item

    @staticmethod
    def find_attr(title, attr_name):
        return mongo.db['items'].find_one({'title': title, 'attributes.attr_name': attr_name})

    @classmethod
    def find_item(cls, title):
        return cls._find_one({'title': title})

    @classmethod
    def find_item_by_id(cls, id):
        return cls._find_one({'_id': id})

    @staticmethod
    def find_items(title=None, limit=20, sorting=pymongo.DESCENDING):
        if title is not None:
            return mongo.db['items'].find({'title': title }).limit(limit).sort('created_at', sorting)
        else:
            return mongo.db['items'].find().limit(limit).sort('created_at', sorting)

    @staticmethod
    def inc_view(title):
        mongo.db['items'].update({'title': title}, {"$inc": {"view": 1}})

    @classmethod
    def create_item(cls, title, type):
        # 返回新增加条目的id
        return cls._create_item(title, type)

    @classmethod
    def del_item(cls, title):
        return cls._del_item({'title': title})

    @classmethod
    def del_item_by_id(cls, id):
        return cls._del_item({'_id': id})

    @classmethod
    def add_attr(cls, title, attr_name, attr_value, attr_type):
        return cls._add_attr({'title': title}, attr_name, attr_value, attr_type)

    @classmethod
    def add_attr_by_id(cls, id, attr_name, attr_value, attr_type):
        return cls._add_attr({'_id': id}, attr_name, attr_value, attr_type)

    @classmethod
    def edit_attr(cls, title, attr_name, attr_value, attr_type):
        return cls._edit_attr({'title': title, "attributes.attr_name": attr_name}, attr_name, attr_value, attr_type)

    @classmethod
    def edit_attr_by_id(cls, id, attr_name, attr_value, attr_type):
        return cls._edit_attr({'_id': id, "attributes.attr_name": attr_name}, attr_name, attr_value, attr_type)

    @classmethod
    def del_attr(cls, title, attr_name):
        return cls._del_attr({'title': title}, attr_name)

    @classmethod
    def del_attr_by_id(cls, title, attr_name):
        return cls._del_attr({'_id': id}, attr_name)
