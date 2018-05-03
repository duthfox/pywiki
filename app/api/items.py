#-*- coding:utf-8 -*-
from app.models import Item
from app.util import bson_to_json, bson_obj_id
from flask import request, jsonify
from flask.views import MethodView

from . import *

import json

# 未测试
class ItemAPI(MethodView):
    def get(self, item_id):
        if item_id is not None:
            item = Item.find_item_by_id(bson_obj_id(item_id))
            return bson_to_json(item)
        params = {}
        for k, v in request.args.items():
            if v:
                Item.add_param(params, k, v)
        cursor = Item._find_many(params)
        items = [bson_to_json(item) for item in cursor]
        return json.dumps(items)

    def post(self):
        item = request.json or {}
        title = item.get('title', None)
        type = item.get('type', None)
        if title and type:
            id = Item.create_item(title, type)
            if id:
                return jsonify(status=True)
            else:
                return jsonify(status=False)
        return jsonify(status=False)


    def put(self, item_id):
        data = request.json or {}
        attr_name = data.get('attr_name', None)
        attr_value = data.get('attr_value', None)
        attr_type = data.get('attr_type', None)
        if item_id and attr_name and attr_value and attr_type:
            if Item.edit_attr_by_id(item_id, attr_name, attr_value, attr_type):
                return jsonify(status=True)
            else:
                return jsonify(status=False)
        return jsonify(status=False)

    def delete(self, item_id):
        if Item.del_item_by_id(item_id):
            return jsonify(status=True)
        else:
            return jsonify(status=False)

item_view = ItemAPI.as_view('item_api')
api.add_url_rule('/items/', defaults={'item_id':None}, view_func=item_view, methods=['GET',])
api.add_url_rule('/items/', view_func=item_view, methods=['POST',])
api.add_url_rule('/items/<item_id>', view_func=item_view, methods=['GET', 'PUT', 'DELETE',])
