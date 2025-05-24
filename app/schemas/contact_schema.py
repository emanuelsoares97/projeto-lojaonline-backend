from email_validator import validate_email, EmailNotValidError

class ContactSchema:
    """Schema para validação de mensagens de contacto"""
    @staticmethod
    def validate(data):
        required_fields = ['name', 'email', 'phone', 'message']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório ausente: {field}")
        
        # Validação do email
        try:
            validate_email(data['email'])
        except EmailNotValidError:
            raise ValueError("Email inválido")
        
        # Validação do telefone (formato básico)
        if not data['phone'].isdigit():
            raise ValueError("O número de telefone deve conter apenas dígitos")
        
        # Validação do tamanho da mensagem
        if len(data['message'].strip()) < 10:
            raise ValueError("A mensagem deve ter pelo menos 10 caracteres") 