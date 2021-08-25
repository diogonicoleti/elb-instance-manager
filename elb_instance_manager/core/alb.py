from boto3 import client as Client


class ALB(object):
    def __init__(self):
        self.client = Client('elbv2')

    def get_instance_ids(self, alb_name):
        response = self.client.describe_target_health(
            TargetGroupArn=self.__get_default_target_group_arn(alb_name))

        return [
            entry['Target']['Id']
            for entry in response['TargetHealthDescriptions']
        ]

    def register(self, alb_name, instance_id):
        self.client.register_targets(
            TargetGroupArn=self.__get_default_target_group_arn(alb_name),
            Targets=[{
                'Id': instance_id
            }])

    def deregister(self, alb_name, instance_id):
        self.client.deregister_targets(
            TargetGroupArn=self.__get_default_target_group_arn(alb_name),
            Targets=[{
                'Id': instance_id
            }])

    def __get_default_target_group_arn(self, alb_name):
        lb_response = self.client.describe_load_balancers(Names=[alb_name])
        tg_response = self.client.describe_target_groups(
            LoadBalancerArn=lb_response['LoadBalancers'][0]['LoadBalancerArn'])
        return tg_response['TargetGroups'][0]['TargetGroupArn']
