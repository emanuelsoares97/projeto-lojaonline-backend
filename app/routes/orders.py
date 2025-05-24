from flask import Blueprint, request, jsonify
from app.schemas.order_schema import OrderSchema
from app.services.email_service import EmailService

bp = Blueprint('orders', __name__)

@bp.route('/api/orders', methods=['POST'])
def create_order():
    """Rota para processar novas encomendas"""
    try:
        data = request.json
        
        # Validação dos dados
        OrderSchema.validate(data)
        
        # Formata e envia o email
        email_body = EmailService.format_order_email(data)
        if EmailService.send_email("Nova Encomenda - LovePulseiras", email_body):
            return jsonify({"message": "Encomenda recebida com sucesso!"}), 200
        else:
            return jsonify({"message": "Erro ao processar encomenda"}), 500

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Erro: {str(e)}"}), 500 