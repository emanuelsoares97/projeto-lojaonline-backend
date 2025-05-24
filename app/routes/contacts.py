from flask import Blueprint, request, jsonify
from app.schemas.contact_schema import ContactSchema
from app.services.email_service import EmailService

bp = Blueprint('contacts', __name__)

@bp.route('/api/contacts', methods=['POST'])
def create_contact():
    """Rota para processar mensagens de contacto"""
    try:
        data = request.json
        
        # Validação dos dados
        ContactSchema.validate(data)
        
        # Formata e envia o email
        email_body = EmailService.format_contact_email(data)
        if EmailService.send_email("Nova Mensagem de Contacto - LovePulseiras", email_body):
            return jsonify({"message": "Mensagem enviada com sucesso!"}), 200
        else:
            return jsonify({"message": "Erro ao enviar mensagem"}), 500

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": f"Erro: {str(e)}"}), 500 