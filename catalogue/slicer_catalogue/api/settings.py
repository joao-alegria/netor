import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'wz3DefHxgQTElMvACRAs1KgAUDPHgTqq')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'
    PORT = 5010
    MONGODB_SETTINGS = {
        'username': os.environ.get('MONGO_USERNAME', 'catalogues'),
        'password': os.environ.get('MONGO_PASSWORD', 'catalogues'),
        'host': os.environ.get('MONGO_URL', 'localhost'),
        'port': 27017,
        'db': os.environ.get('MONGO_DB', 'catalogues')
    }


class AuthConfig:
    IDP_IP = os.getenv("IDP_IP", "localhost")
    IDP_PORT = os.getenv("IDP_PORT", 5002)
    IDP_ENDPOINT = os.getenv("IDP_ENDPOINT", "/validate")


class ProdConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'prod'


class DevConfig(Config):
    """Development configurations"""
    DEBUG = True
    ENV = 'dev'
