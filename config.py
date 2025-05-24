import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
    EMAIL_FROM = config('EMAIL_FROM')
    EMAIL_PASSWORD = config('EMAIL_PASSWORD')
    EMAIL_TO = config('EMAIL_TO')

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True

class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False

config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig
}

def get_config():
    env = os.getenv('FLASK_ENV', 'dev')
    return config_by_name[env] 