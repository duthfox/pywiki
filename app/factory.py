#-*- coding:utf-8 -*-
from flask import Flask
from flask.ext.login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
from app.config import config
from app.extensions import admin, mongo, mail, login_manager, celery
from app.models import User
from app.util import bson_obj_id

import os

class FileView(FileAdmin):
    def is_accessible(self):
        return not current_user.is_anonymous and current_user.is_admin

def create_app(config_name='dev'):
    app = Flask(__name__)
    # sifn = show if none
    app.jinja_env.filters['sifn'] = lambda it: '无' if not it else it
    app.jinja_env.filters['with_site'] = lambda title: title + ' - pkyx'
    # 导入配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    # 初始化flask_admin
    admin.init_app(app)
    admin.add_view(FileView(os.path.join(os.path.dirname(__file__), 'static'), '/static/'))
    # 初始化MongoDB
    mongo.init_app(app)
    with app.app_context():
        mongo.db['items'].create_index('title', background=True)
    # 初始化Celery
    celery.init_app(app)
    # 初始化Flask-mail
    mail.init_app(app)
    # 初始化Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'main.register'
    login_manager.login_message = '请先登录或注册'

    @login_manager.user_loader
    def load_user(user_id):
        user = None
        db_user = mongo.db.users.find_one({"_id": bson_obj_id(user_id)})
        if db_user is not None:
            user_id = db_user.pop('_id')
            user = User(user_id, extras=db_user)
        return user

    # @login_manager.unauthorized_handler
    # def unauthorized():
    #   pass


    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
