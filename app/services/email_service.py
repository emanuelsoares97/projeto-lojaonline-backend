import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

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