import os
from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('EMAIL_FROM')
    MAIL_PASSWORD = config('EMAIL_PASSWORD')
    MAIL_RECEIVER = config('EMAIL_TO')

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