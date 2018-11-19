import datetime


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

    DEBUG = False

    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "Rock"

    PERMANENT_SESSION_LIFETIME = datetime.timedelta(14)


class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "GP1FlaskModel"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestConfig(Config):
    TESTING = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "GP1FlaskModel"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagineConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "GP1FlaskModel"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "rock1204",
        "HOST": "localhost",
        "PORT": "3306",
        "NAME": "GP1FlaskModel"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestConfig,
    "staging": StagineConfig,
    "product": ProductConfig,
    "default": DevelopConfig,
}