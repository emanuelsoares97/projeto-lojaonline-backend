from marshmallow import Schema, fields, validate

class ItemSchema(Schema):
    nome = fields.Str(required=True)
    preco = fields.Float(required=True, validate=validate.Range(min=0))
    quantidade = fields.Int(required=True, validate=validate.Range(min=1))
    imagem = fields.Str(required=True)

class EncomendaSchema(Schema):
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))
    total = fields.Float(required=True, validate=validate.Range(min=0))
    data = fields.Str(allow_none=True)
    cliente = fields.Str(allow_none=True)
    email_cliente = fields.Email(allow_none=True)
    morada_entrega = fields.Str(allow_none=True)
    telefone = fields.Str(allow_none=True)

    class Meta:
        unknown = True  # Permite campos adicionais 