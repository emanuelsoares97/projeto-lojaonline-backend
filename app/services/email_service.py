import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from app.utils.logger_utils import get_logger

logger = get_logger(__name__)

class EmailService:
    """Serviço para envio de emails"""
    @staticmethod
    def send_email(subject, body, recipient=None):
        """Envia email usando SMTP do Gmail"""
        sender = current_app.config['EMAIL_FROM']
        password = current_app.config['EMAIL_PASSWORD']
        recipient = recipient or current_app.config['EMAIL_TO']

        # Configuração da mensagem
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject

        # Adiciona o corpo do email
        msg.attach(MIMEText(body, 'html'))

        # Envia o email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False

    @staticmethod
    def format_order_email(order_data):
        """Formata o email para encomendas"""
        items_html = "<ul>"
        for item in order_data['items']:
            items_html += f"""
                <li>
                    {item['name']} - Quantidade: {item['quantity']} - 
                    Preço: {item['price']}€ - Total: {item['total_item']}€
                </li>
            """
        items_html += "</ul>"

        return f"""
        <h2>Nova Encomenda Recebida!</h2>
        <p><strong>Cliente:</strong> {order_data['client']}</p>
        <p><strong>Data:</strong> {order_data['date']}</p>
        <p><strong>Itens:</strong></p>
        {items_html}
        <p><strong>Total da Encomenda:</strong> {order_data['total']}€</p>
        """

    @staticmethod
    def format_contact_email(contact_data):
        """Formata o email para mensagens de contacto"""
        return f"""
        <h2>Nova Mensagem de Contacto</h2>
        <p><strong>Nome:</strong> {contact_data['name']}</p>
        <p><strong>Email:</strong> {contact_data['email']}</p>
        <p><strong>Número:</strong> {contact_data['phone']}</p>
        <p><strong>Mensagem:</strong></p>
        <p>{contact_data['message']}</p>
        """

    @staticmethod
    def enviar_email_encomenda(encomenda):
        try:
            if not current_app.config['MAIL_USERNAME'] or not current_app.config['MAIL_PASSWORD']:
                logger.error("Configurações de email não definidas no servidor")
                raise Exception("Configurações de email não definidas no servidor")

            msg = MIMEMultipart()
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = current_app.config['MAIL_RECEIVER']
            msg['Subject'] = "Nova Encomenda - LovePulseiras"

            # Criar o corpo do email
            corpo = "Nova Encomenda Recebida!\n\n"
            corpo += f"Data: {encomenda.get('data', 'N/A')}\n"
            
            # Adicionar informações do cliente se disponíveis
            if encomenda.get('cliente'):
                corpo += f"Cliente: {encomenda['cliente']}\n"
            if encomenda.get('email_cliente'):
                corpo += f"Email do Cliente: {encomenda['email_cliente']}\n"
            if encomenda.get('morada_entrega'):
                corpo += f"Morada de Entrega: {encomenda['morada_entrega']}\n"
            if encomenda.get('telefone'):
                corpo += f"Telefone: {encomenda['telefone']}\n"
            
            corpo += "\nItems:\n"
            for item in encomenda['items']:
                corpo += f"- {item['nome']} (Quantidade: {item['quantidade']}) - {item['preco']}€\n"
            
            corpo += f"\nTotal da Encomenda: {encomenda['total']}€"

            msg.attach(MIMEText(corpo, 'plain'))

            logger.info(f"Preparando para enviar email para {current_app.config['MAIL_RECEIVER']}")

            with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.starttls()
                server.login(
                    current_app.config['MAIL_USERNAME'],
                    current_app.config['MAIL_PASSWORD']
                )
                server.send_message(msg)
                logger.info("Email enviado com sucesso")

        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) 