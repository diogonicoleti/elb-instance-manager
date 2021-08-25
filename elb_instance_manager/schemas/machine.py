from marshmallow import Schema, fields


class MachineInfoSchema(Schema):
    InstanceId = fields.Str(required=True, data_key="instanceId")
    InstanceType = fields.Str(required=True, data_key="instanceType")
    LaunchTime = fields.Str(required=True, data_key="launchDate")

    class Meta:
        ordered = True


class MachineIdSchema(Schema):
    InstanceId = fields.Str(required=True, data_key="instanceId")
