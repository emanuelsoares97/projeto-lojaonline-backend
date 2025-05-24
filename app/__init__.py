from flask import Flask
from flask_cors import CORS
from config import get_config

def create_app():
    """Função de fábrica da aplicação Flask"""
    app = Flask(__name__)
    
    # Carregar configuração baseada no ambiente
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Inicialização de extensões
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Registro de blueprints
    from app.routes import orders_bp
    from app.routes.contacts import contacts_bp
    
    app.register_blueprint(orders_bp)
    app.register_blueprint(contacts_bp)
    
    return app 