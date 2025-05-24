from flask import Blueprint, jsonify, request
from datetime import datetime
from app.schemas import EncomendaSchema
from app.services.email_service import EmailService
from marshmallow import ValidationError

encomendas_bp = Blueprint('encomendas', __name__)

@encomendas_bp.route('/')
def home():
    """
    Rota raiz para verificar se a API está funcionando
    """
    return jsonify({
        "message": "Bem-vindo à API da LovePulseiras",
        "status": "online"
    })

@encomendas_bp.route('/fazer-encomenda', methods=['POST'])
def fazer_encomenda():
    """
    Processa uma nova encomenda e envia email de notificação
    """
    try:
        # Validar dados da encomenda
        schema = EncomendaSchema()
        data = request.get_json()
        
        if not data:
            return jsonify({
                "message": "Dados da encomenda não fornecidos",
                "status": "error"
            }), 400
        
        # Validar e deserializar dados
        encomenda = schema.load(data)
        
        # Adicionar data se não fornecida
        if not encomenda.get('data'):
            encomenda['data'] = datetime.now().strftime("%Y-%m-%d")
        
        # Enviar email
        EmailService.enviar_email_encomenda(encomenda)
        
        return jsonify({
            "message": "Encomenda processada com sucesso!",
            "status": "success",
            "data": encomenda
        })
        
    except ValidationError as err:
        return jsonify({
            "message": "Erro de validação dos dados",
            "status": "error",
            "errors": err.messages
        }), 400
        
    except Exception as e:
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500 