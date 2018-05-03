import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BaseConfig:
    SECRET_KEY = '693bda65112eb4b1eab2bfe3fa8e672ad220fa7c'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAIL_SUBJECT_PREFIX = '[PYWIKI]'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'g1226cl@163.com' 
    MAIL_PASSWORD = 'g1226cl'
    MAIL_DEFAULT_SENDER = 'g1226cl@163.com'

    @staticmethod
    def init_app(app):
        pass

class DevConfig(BaseConfig):
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_DBNAME = 'pywiki'
    CELERY_IMPORTS = (
        "app.tasks.mail",
    )
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass

config = {
    'dev': DevConfig,
}
