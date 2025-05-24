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
    def send_order_email(order):
        """Envia email de notificação de nova encomenda"""
        try:
            if not current_app.config.get('EMAIL_FROM') or not current_app.config.get('EMAIL_PASSWORD'):
                logger.error("Configurações de email não definidas no servidor")
                raise Exception("Configurações de email não definidas no servidor")

            msg = MIMEMultipart()
            msg['From'] = current_app.config['EMAIL_FROM']
            msg['To'] = current_app.config['EMAIL_TO']
            msg['Subject'] = "Nova Encomenda - LovePulseiras"

            # Criar o corpo do email em HTML
            items_html = "<ul>"
            for item in order['items']:
                items_html += f"""
                    <li>
                        {item['name']} - Quantidade: {item['quantity']} - 
                        Preço: {item['price']}€
                    </li>
                """
            items_html += "</ul>"

            body = f"""
            <h2>Nova Encomenda Recebida!</h2>
            <p><strong>Data:</strong> {order.get('date', 'N/A')}</p>
            """

            if order.get('customer'):
                body += f"<p><strong>Cliente:</strong> {order['customer']}</p>"
            if order.get('customer_email'):
                body += f"<p><strong>Email do Cliente:</strong> {order['customer_email']}</p>"
            if order.get('delivery_address'):
                body += f"<p><strong>Morada de Entrega:</strong> {order['delivery_address']}</p>"
            if order.get('phone'):
                body += f"<p><strong>Telefone:</strong> {order['phone']}</p>"

            body += f"""
            <p><strong>Itens:</strong></p>
            {items_html}
            <p><strong>Total da Encomenda:</strong> {order['total']}€</p>
            """

            msg.attach(MIMEText(body, 'html'))

            logger.info(f"Preparando para enviar email para {current_app.config['EMAIL_TO']}")

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(
                    current_app.config['EMAIL_FROM'],
                    current_app.config['EMAIL_PASSWORD']
                )
                server.send_message(msg)
                logger.info("Email enviado com sucesso")

        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg) 