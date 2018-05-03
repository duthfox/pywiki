from flask.ext.pymongo import PyMongo
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.celery import Celery
from flask.ext.admin import Admin

admin = Admin()
mail = Mail()
mongo = PyMongo()
celery = Celery()
login_manager = LoginManager()

