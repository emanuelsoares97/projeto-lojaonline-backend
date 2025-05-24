import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from app.utils.logger_utils import get_logger
import traceback

logger = get_logger(__name__)

class EmailService:
    """Serviço para envio de emails"""
    
    @staticmethod
    def send_order_email(order):
        """Envia email de notificação de nova encomenda"""
        try:
            # Log detalhado das configurações
            logger.info("Verificando configurações de email...")
            logger.info(f"EMAIL_FROM configurado: {'Sim' if current_app.config.get('EMAIL_FROM') else 'Não'}")
            logger.info(f"EMAIL_TO configurado: {'Sim' if current_app.config.get('EMAIL_TO') else 'Não'}")
            logger.info(f"EMAIL_PASSWORD configurado: {'Sim' if current_app.config.get('EMAIL_PASSWORD') else 'Não'}")
            
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

            if order.get('login_name'):
                body += f"<p><strong>Cliente:</strong> {order['login_name']}</p>"
            elif order.get('customer'):
                body += f"<p><strong>Cliente:</strong> {order['customer']}</p>"
            if order.get('phone'):
                body += f"<p><strong>Telefone:</strong> {order['phone']}</p>"

            body += f"""
            <p><strong>Itens:</strong></p>
            {items_html}
            <p><strong>Total da Encomenda:</strong> {order['total']}€</p>
            """

            msg.attach(MIMEText(body, 'html'))

            logger.info(f"Preparando para enviar email para {current_app.config['EMAIL_TO']}")

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    logger.info("Conectando ao servidor SMTP...")
                    server.starttls()
                    logger.info("Iniciando login...")
                    server.login(
                        current_app.config['EMAIL_FROM'],
                        current_app.config['EMAIL_PASSWORD']
                    )
                    logger.info("Login bem sucedido, enviando email...")
                    server.send_message(msg)
                    logger.info("Email enviado com sucesso")
            except Exception as smtp_error:
                logger.error(f"Erro SMTP detalhado: {str(smtp_error)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise

        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            raise Exception(error_msg)

    @staticmethod
    def send_contact_email(msg_data):
        """Envia email de notificação de nova mensagem de contato"""
        try:
            # Log detalhado das configurações
            logger.info("Verificando configurações de email...")
            logger.info(f"EMAIL_FROM configurado: {'Sim' if current_app.config.get('EMAIL_FROM') else 'Não'}")
            logger.info(f"EMAIL_TO configurado: {'Sim' if current_app.config.get('EMAIL_TO') else 'Não'}")
            logger.info(f"EMAIL_PASSWORD configurado: {'Sim' if current_app.config.get('EMAIL_PASSWORD') else 'Não'}")
            
            if not current_app.config.get('EMAIL_FROM') or not current_app.config.get('EMAIL_PASSWORD'):
                logger.error("Configurações de email não definidas no servidor")
                raise Exception("Configurações de email não definidas no servidor")

            msg = MIMEMultipart()
            msg['From'] = current_app.config['EMAIL_FROM']
            msg['To'] = current_app.config['EMAIL_TO']
            msg['Subject'] = msg_data['subject']

            msg.attach(MIMEText(msg_data['body'], 'html'))

            logger.info(f"Preparando para enviar email para {current_app.config['EMAIL_TO']}")

            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    logger.info("Conectando ao servidor SMTP...")
                    server.starttls()
                    logger.info("Iniciando login...")
                    server.login(
                        current_app.config['EMAIL_FROM'],
                        current_app.config['EMAIL_PASSWORD']
                    )
                    logger.info("Login bem sucedido, enviando email...")
                    server.send_message(msg)
                    logger.info("Email enviado com sucesso")
            except Exception as smtp_error:
                logger.error(f"Erro SMTP detalhado: {str(smtp_error)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise

        except Exception as e:
            error_msg = f"Erro ao enviar email: {str(e)}"
            logger.error(error_msg)
            logger.error(f"Traceback completo: {traceback.format_exc()}")
            raise Exception(error_msg) 