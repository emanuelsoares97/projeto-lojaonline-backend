from flask import Blueprint, jsonify, request, current_app
from app.services.email_service import EmailService
from app.utils.logger_utils import get_logger
from marshmallow import Schema, fields, ValidationError

logger = get_logger(__name__)

# Schema para validação dos dados do contato
class ContactSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    message = fields.Str(required=True)

contacts_bp = Blueprint('contacts', __name__, url_prefix='/api')

@contacts_bp.route('/contacts', methods=['POST'])
def create_contact():
    """
    Processa uma nova mensagem de contato
    """
    try:
        # Validar dados do contato
        schema = ContactSchema()
        data = request.get_json()
        
        if not data:
            logger.warning("Requisição recebida sem dados")
            return jsonify({
                "message": "Dados do contato não fornecidos",
                "status": "error"
            }), 400
        
        logger.debug(f"Dados recebidos: {data}")
        
        try:
            # Validar e deserializar dados
            contact = schema.load(data)
            logger.info("Dados do contato validados com sucesso")
        except ValidationError as err:
            logger.error(f"Erro de validação: {err.messages}")
            return jsonify({
                "message": "Erro de validação dos dados",
                "status": "error",
                "errors": err.messages
            }), 400
        
        # Preparar o corpo do email
        email_body = f"""
        <h2>Nova Mensagem de Contato Recebida!</h2>
        <p><strong>Nome:</strong> {contact['name']}</p>
        <p><strong>Email:</strong> {contact['email']}</p>
        <p><strong>Telefone:</strong> {contact['phone']}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{contact['message']}</p>
        """

        # Enviar email
        try:
            msg = {
                'subject': 'Nova Mensagem de Contato - LovePulseiras',
                'body': email_body,
                'is_contact': True  # Flag para identificar que é um email de contato
            }
            EmailService.send_contact_email(msg)
            logger.info("Mensagem de contato processada e email enviado com sucesso")
        except Exception as email_error:
            logger.error(f"Erro ao enviar email: {str(email_error)}")
            return jsonify({
                "message": f"Erro ao enviar email: {str(email_error)}",
                "status": "error"
            }), 500
        
        return jsonify({
            "message": "Mensagem enviada com sucesso!",
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Erro ao processar mensagem de contato: {str(e)}")
        return jsonify({
            "message": str(e),
            "status": "error"
        }), 500 