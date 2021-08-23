from boto3 import client, resource
from botocore.exceptions import ClientError
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from schemas import MachineIdSchema

machine_id_schema = MachineIdSchema()


class ELB(Resource):
    def __init__(self):
        self.elb = client('elbv2')
        self.ec2 = resource('ec2')

    def get(self, elb_name):
        try:
            load_balancer = self.elb.describe_load_balancers(
                Names=[elb_name])

            return load_balancer['LoadBalancers'][0]['LoadBalancerArn'], 200
        except ClientError as err:
            if err.response['Error']['Code'] == 'LoadBalancerNotFound':
                return 'Load Balancer not found', 404
            else:
                raise err

    def post(self, elb_name):
        try:
            machineId = machine_id_schema.load(request.get_json())
        except ValidationError:
            return 'Wrong data format', 400

    def delete(self, elb_name):
        try:
            machineId = machine_id_schema.load(request.get_json())
        except ValidationError:
            return 'Wrong data format', 400
