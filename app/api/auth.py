from app.extensions import mongo
from app.models import User
from flask import g, jsonify
from flask.ext.httpauth import HTTPBasicAuth

from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    user = User.verify_auth_token(email_or_token)
    if user is None:
        user = mongo.db.users.find_one({'email': email_or_token})
        if not user:
            return False
        else:
            if not User.verify_passwd(user['password'], password):
                return False
    g.current_user = User(user.pop("_id"), extras=user)
    return True

@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.current_user.gen_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@api.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.current_user.username})