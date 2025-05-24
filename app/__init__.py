from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config

def create_app():
    """Função de fábrica da aplicação Flask"""
    app = Flask(__name__)
    
    # Carregar configuração baseada no ambiente
    config_class = get_config()
    app.config.from_object(config_class)
    
    # Inicialização de extensões
    CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Accept"]
}})
    
    # Rota raiz para verificar se a API está funcionando
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "API Love Pulseiras está online!"
        })
    
    # Registro de blueprints
    from app.routes import orders_bp
    from app.routes.contacts import contacts_bp
    
    app.register_blueprint(orders_bp)
    app.register_blueprint(contacts_bp)
    
    return app 