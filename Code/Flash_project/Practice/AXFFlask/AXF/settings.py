import os
import redis
from flask_uploads import IMAGES

from AXF.config import SERVER_HOST, SERVER_PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_uri(dbinfo):

    engine = dbinfo.get("ENGINE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:

    TESTING = False

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "qiao"
    SESSION_TYPE = "redis"
    # SESSION_COOKIE_SECURE = True
    # SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='123456')

    CACHE_REDIS_URL = 'redis://:123456@localhost:6379/1'

    MAIL_SERVER = "smtp.163.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "qiaodan0919@163.com"
    MAIL_PASSWORD = "qd970919"
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    UPLOADED_PHOTO_DEST = BASE_DIR + '/static/uploads/icons'
    UPLOADED_PHOTO_ALLOW = IMAGES
    UPLOADS_DEFAULT_URL = 'http://{}:{}/'.format(SERVER_HOST, SERVER_PORT)


class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "AXFFlask"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):

    TESTINE = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "AXFFlask"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "AXFFlask"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "AXFFlask"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}
