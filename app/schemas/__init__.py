from marshmallow import Schema, fields, validate

class ItemSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    image = fields.Str(required=True)

class OrderSchema(Schema):
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))
    total = fields.Float(required=True, validate=validate.Range(min=0))
    date = fields.Str(allow_none=True)
    customer = fields.Str(allow_none=True)
    customer_email = fields.Email(allow_none=True)
    delivery_address = fields.Str(allow_none=True)
    phone = fields.Str(allow_none=True)

    class Meta:
        unknown = True  # Permite campos adicionais
