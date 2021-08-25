from boto3 import client as Client


class EC2(object):
    def __init__(self):
        self.client = Client('ec2')

    def get_instances(self, instance_ids):
        response = self.client.describe_instances(InstanceIds=instance_ids)
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances.append(instance)

        return instances

    def get_instance(self, instance_id):
        return self.get_instances([instance_id])[0]
