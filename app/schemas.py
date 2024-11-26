from marshmallow import Schema, fields

class AccountSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    balance = fields.Float(dump_only=True)
