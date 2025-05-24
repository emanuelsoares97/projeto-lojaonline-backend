import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações base da aplicação"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret'
    EMAIL_FROM = os.environ.get('EMAIL_FROM')
    EMAIL_TO = os.environ.get('EMAIL_TO')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    PORT = int(os.environ.get('PORT', 5000))

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False

# Dicionário para selecionar a configuração baseado no ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 