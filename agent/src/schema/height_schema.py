from marshmallow import Schema, fields


class HeightSchema(Schema):
    height = fields.Float()
