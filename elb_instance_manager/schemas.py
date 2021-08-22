from marshmallow import Schema, fields


class MachineInfoSchema(Schema):
    instanceId = fields.Str(required=True)
    instanceType = fields.Str(required=True)
    launchDate = fields.Str(required=True)


class MachineIdSchema(Schema):
    instanceId = fields.Str(required=True)
