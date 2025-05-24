from flask import Flask
from flask_cors import CORS
from app.config import Config

def create_app(config_class=Config):
    """Função de fábrica da aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicialização de extensões
    CORS(app)
    
    # Registro de blueprints
    from app.routes import orders, contacts
    app.register_blueprint(orders.bp)
    app.register_blueprint(contacts.bp)
    
    return app 