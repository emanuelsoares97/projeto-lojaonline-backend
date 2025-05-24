import os
from decouple import config

class Config:
    """Configuração base"""
    SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
    EMAIL_FROM = config('EMAIL_FROM', default=None)
    EMAIL_PASSWORD = config('EMAIL_PASSWORD', default=None)
    EMAIL_TO = config('EMAIL_TO', default=None)

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    DEVELOPMENT = True

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    DEVELOPMENT = False

def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.getenv('FLASK_ENV', 'dev')
    
    if env == 'prod':
        return ProductionConfig()
    
    return DevelopmentConfig() 