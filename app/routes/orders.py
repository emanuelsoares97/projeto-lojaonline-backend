from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
from app.schemas import OrderSchema
from app.services.email_service import EmailService
from marshmallow import ValidationError
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

orders_bp = Blueprint('orders', __name__, url_prefix='/api')


@orders_bp.route('/')
def home():
    """
    Rota raiz para verificar se a API está funcionando
    """
    logger.info("Acesso à rota raiz")
    return jsonify({
        "message": "Bem-vindo à API da LovePulseiras",
        "status": "online"
    })

@orders_bp.route('/orders', methods=['OPTIONS'])
def handle_options():
    """
    Rota para lidar com requisições OPTIONS (preflight CORS)
    """
    response = current_app.make_default_options_response()
    return response

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """
    Processa uma nova encomenda e envia email de notificação
    """
    try:
        # Log das configurações de email (sem a senha)
        logger.info(f"Email From: {current_app.config.get('EMAIL_FROM')}")
        logger.info(f"Email To: {current_app.config.get('EMAIL_TO')}")
        
        # Validar dados da encomenda
        schema = OrderSchema()
        data = request.get_json()
        
        if not data:
            logger.warning("Requisição recebida sem dados")
            return jsonify({
                "message": "Dados da encomenda não fornecidos",
                "status": "error"
            }), 400
        
        logger.debug(f"Dados recebidos: {data}")
        
        try:
            # Validar e deserializar dados
            order = schema.load(data)
            logger.info("Dados da encomenda validados com sucesso")
        except ValidationError as err:
            logger.error(f"Erro de validação: {err.messages}")
            return jsonify({
                "message": "Erro de validação dos dados",
                "status": "error",
                "errors": err.messages
            }), 400
        
        # Adicionar data se não fornecida
        if not order.get('date'):
            order['date'] = datetime.now().strftime("%Y-%m-%d")
        
        try:
            # Enviar email
            EmailService.send_order_email(order)
            logger.info("Encomenda processada e email enviado com sucesso")
        except Exception as email_error:
            logger.error(f"Erro ao enviar email: {str(email_error)}")
            return jsonify({
                "message": f"Erro ao enviar email: {str(email_error)}",
                "status": "error"
            }), 500
        
        return jsonify({
            "message": "Encomenda processada com sucesso!",
            "status": "success",
            "data": order
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar encomenda: {str(e)}")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500 