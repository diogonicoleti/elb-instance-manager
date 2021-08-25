import logging
from botocore.exceptions import ClientError
from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from core.alb import ALB
from core.ec2 import EC2
from schemas.machine import MachineIdSchema, MachineInfoSchema
from schemas.error import ErrorResponseSchema

errResponseSchema = ErrorResponseSchema()


class ELBResource(Resource):
    def __init__(self):
        self.alb = ALB()
        self.ec2 = EC2()

    def get(self, elb_name):
        try:
            alb_instance_ids = self.alb.get_instance_ids(elb_name)
            instances = self.ec2.get_instances(
                alb_instance_ids) if alb_instance_ids else []
            return MachineInfoSchema(many=True).dump(instances), 200
        except ClientError as err:
            return self.__handle_client_error(err)

    def post(self, elb_name):
        try:
            id = self.__get_instance_id()
            if id in self.alb.get_instance_ids(elb_name):
                return self.__get_validation_error(
                    'Instance already on load balancer'), 409

            self.alb.register(elb_name, id)
            return self.__get_instance(id), 201
        except ValidationError:
            return self.__get_validation_error('Wrong data format'), 400
        except ClientError as err:
            return self.__handle_client_error(err)

    def delete(self, elb_name):
        try:
            id = self.__get_instance_id()
            if id not in self.alb.get_instance_ids(elb_name):
                return self.__get_validation_error(
                    'Instance is not on load balancer'), 409

            self.alb.deregister(elb_name, id)
            return self.__get_instance(id), 201
        except ValidationError:
            return self.__get_validation_error('Wrong data format'), 400
        except ClientError as err:
            return self.__handle_client_error(err)

    def __get_instance(self, instance_id):
        return MachineInfoSchema().dump(self.ec2.get_instance(instance_id))

    def __get_instance_id(self):
        return MachineIdSchema().load(request.get_json())

    def __get_validation_error(self, message):
        return errResponseSchema.dump({
            'Code': 'ValidationError',
            'Message': message
        })

    def __handle_client_error(self, err):
        if err.response['Error']['Code'] == 'LoadBalancerNotFound':
            return errResponseSchema.dump(err.response['Error']), 404
        if err.response['Error']['Code'] in ('ValidationError',
                                             'InvalidTarget'):
            return errResponseSchema.dump(err.response['Error']), 400

        logging.error('Unexpected error: %s' % err)
        return errResponseSchema.dump(err.response['Error']), 500
