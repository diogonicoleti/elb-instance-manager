from boto3 import client as Client


class EC2(object):
    def __init__(self):
        self.client = Client('ec2')

    def get_instances(self, instance_ids):
        response = self.client.describe_instances(InstanceIds=instance_ids)
        return response['Reservations'][0]['Instances']
