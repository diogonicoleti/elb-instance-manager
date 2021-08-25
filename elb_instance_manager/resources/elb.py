from botocore.exceptions import ClientError
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from core.alb import ALB
from core.ec2 import EC2
from schemas.machine import MachineIdSchema, MachineInfoSchema


class ELBResource(Resource):
    def __init__(self):
        self.alb = ALB()
        self.ec2 = EC2()

    def get(self, elb_name):
        try:
            alb_instance_ids = self.alb.get_instance_ids(elb_name)
            instances = self.ec2.get_instances(alb_instance_ids) if alb_instance_ids else []
            return MachineInfoSchema(many=True).dump(instances), 200
        except ClientError as err:
            if err.response['Error']['Code'] == 'LoadBalancerNotFound':
                return 'Load Balancer not found', 404
            else:
                raise err

    def post(self, elb_name):
        try:
            id = self.__get_instance_id()
            self.alb.register(elb_name, id)
            return self.__get_instance(id), 200
        except ValidationError:
            return 'Wrong data format', 400

    def delete(self, elb_name):
        try:
            id = self.__get_instance_id()
            self.alb.deregister(elb_name, id)
            return self.__get_instance(id), 200
        except ValidationError:
            return 'Wrong data format', 400

    def __get_instance(self, instance_id):
        return MachineInfoSchema().dump(self.ec2.get_instance(instance_id))

    def __get_instance_id(self):
        return MachineIdSchema().load(request.get_json())
