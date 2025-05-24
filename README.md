# API LovePulseiras

API em Flask para processar encomendas e mensagens de contacto da loja LovePulseiras.

## Configuração

1. Instale as dependências:
```bash
pip install -r requirements.txt
```


## Rotas Disponíveis

### POST /api/fazer-encomenda
Processa novas encomendas e envia email de confirmação.

Exemplo de payload:
```json
{
  "items": [
    {
      "nome": "Produto 1",
      "quantidade": 2,
      "preco": 10.99,
      "total_item": 21.98
    }
  ],
  "total": 21.98,
  "cliente": "Nome do Cliente",
  "data": "2024-02-20T15:30:00"
}
```

### POST /api/contacto
Processa mensagens do formulário de contacto.

Exemplo de payload:
```json
{
  "nome": "Nome do Cliente",
  "email": "cliente@email.com",
  "numero": "123456789",
  "mensagem": "Mensagem do cliente"
}
```

## Executar Localmente

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Deploy

Esta API está preparada para deploy no Render. Configure as variáveis de ambiente no painel do Render antes de fazer o deploy. 