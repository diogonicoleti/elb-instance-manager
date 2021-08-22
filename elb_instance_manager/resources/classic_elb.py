from boto3 import client, resource
from botocore.exceptions import ClientError
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from schemas import MachineIdSchema

machine_id_schema = MachineIdSchema()


class ClassicELB(Resource):
    def __init__(self):
        self.elb = client('elb')
        self.ec2 = resource('ec2')

    def get(self, elb_name):
        try:
            load_balancer = self.elb.describe_load_balancers(
                LoadBalancerNames=[elb_name])

            machineInfos = []
            for instance in load_balancer['LoadBalancerDescriptions'][0]['Instances']:
                machineInfos.append(
                    self.__get_instance_info(instance['InstanceId']))

            return machineInfos, 200
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

        try:
            instance_id = machineId['instanceId']
            self.elb.register_instances_with_load_balancer(
                LoadBalancerName=elb_name,
                Instances=[{
                    'InstanceId': instance_id
                }])

            return self.__get_instance_info(instance_id), 201
        except ClientError as err:
            if err.response['Error']['Code'] == 'InvalidInstance':
                return 'Instance does not exists or is invalid', 400
            else:
                raise err

    def delete(self, elb_name):
        try:
            machineId = machine_id_schema.load(request.get_json())
        except ValidationError:
            return 'Wrong data format', 400

        try:
            instance_id = machineId['instanceId']
            self.elb.deregister_instances_from_load_balancer(
                LoadBalancerName=elb_name,
                Instances=[{
                    'InstanceId': instance_id
                }])

            return self.__get_instance_info(instance_id), 201
        except ClientError as err:
            if err.response['Error']['Code'] == 'InvalidInstance':
                return 'Instance does not exists or is invalid', 400
            else:
                raise err

    def __get_instance_info(self, instance_id):
        instance = self.ec2.Instance(instance_id)
        instance.load()
        return {
            'instanceId': instance.instance_id,
            'instanceType': instance.instance_type,
            'launchDate': instance.launch_time.isoformat()
        }
