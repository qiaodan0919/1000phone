import os

import redis
from flask_uploads import IMAGES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_uri(dbinfo):

    engine = dbinfo.get("ENGINE") or "sqlite"
    driver = dbinfo.get("DRIVER") or "sqlite"
    user = dbinfo.get("USER") or ""
    password = dbinfo.get("PASSWORD") or ""
    host = dbinfo.get("HOST") or ""
    port = dbinfo.get("PORT") or ""
    name = dbinfo.get("NAME") or ""

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:

    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "qiao"
    SESSION_TYPE = "redis"
    SESSION_COOKIE_SECURE = True
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port='6379', password='123456')

    UPLOADED_PHOTO_DEST = os.path.dirname(os.path.abspath(__file__))
    UPLOADED_PHOTO_ALLOW = IMAGES


class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskTwo"

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    TESTING = True

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskTwo"

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskTwo"

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    dbinfo = {

        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "qd970919-",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "FlaskTwo"

    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}