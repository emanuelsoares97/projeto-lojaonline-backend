from datetime import datetime

class OrderSchema:
    """Schema para validação de encomendas"""
    @staticmethod
    def validate(data):
        required_fields = ['items', 'total', 'client', 'date']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo obrigatório ausente: {field}")
        
        if not isinstance(data['items'], list):
            raise ValueError("O campo 'items' deve ser uma lista")
        
        for item in data['items']:
            if not all(key in item for key in ['name', 'quantity', 'price', 'total_item']):
                raise ValueError("Campos obrigatórios ausentes no item")
            
            if not isinstance(item['quantity'], int):
                raise ValueError("A quantidade deve ser um número inteiro")
            
            if not isinstance(item['price'], (int, float)):
                raise ValueError("O preço deve ser um número")
            
            if not isinstance(item['total_item'], (int, float)):
                raise ValueError("O total do item deve ser um número")
        
        try:
            datetime.fromisoformat(data['date'])
        except ValueError:
            raise ValueError("Data inválida") 