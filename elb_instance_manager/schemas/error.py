from marshmallow import Schema, fields


class ErrorResponseSchema(Schema):
    Code = fields.Str(required=True, data_key='error')
    Message = fields.Str(required=True, data_key='message')

    class Meta:
        ordered = True
