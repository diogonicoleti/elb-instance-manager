import pytest

from elb_instance_manager.core.alb import ALB
from tests.helpers import assert_ec2_instance
from tests import EXAMPLE_AMI_ID

ALB_NAME = 'default-alb'


@pytest.fixture
def mocked_instance_ids(ec2_client):
    reservation = ec2_client.run_instances(ImageId=EXAMPLE_AMI_ID,
                                           InstanceType='t3.micro',
                                           MaxCount=5,
                                           MinCount=5)
    return [instance['InstanceId'] for instance in reservation['Instances']]


@pytest.fixture
def mocked_alb(ec2_client, elbv2_client, mocked_instance_ids):
    vpc = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    subnet_a = ec2_client.create_subnet(VpcId=vpc['Vpc']['VpcId'],
                                        CidrBlock="10.0.0.0/24",
                                        AvailabilityZone="us-east-1a")
    subnet_b = ec2_client.create_subnet(VpcId=vpc['Vpc']['VpcId'],
                                        CidrBlock="10.0.1.0/24",
                                        AvailabilityZone="us-east-1b")
    alb = elbv2_client.create_load_balancer(Name=ALB_NAME,
                                            Subnets=[
                                                subnet_a['Subnet']['SubnetId'],
                                                subnet_b['Subnet']['SubnetId']
                                            ])

    target_group = elbv2_client.create_target_group(Name="http",
                                                    Protocol="HTTP",
                                                    Port=80,
                                                    VpcId=vpc['Vpc']['VpcId'])

    alb_arn = alb['LoadBalancers'][0]['LoadBalancerArn']
    target_group_arn = target_group['TargetGroups'][0]['TargetGroupArn']

    elbv2_client.create_listener(LoadBalancerArn=alb_arn,
                                 Protocol="HTTP",
                                 Port=80,
                                 DefaultActions=[{
                                     "Type":
                                     "forward",
                                     "TargetGroupArn":
                                     target_group_arn
                                 }])
    elbv2_client.register_targets(TargetGroupArn=target_group_arn,
                                  Targets=[
                                      {
                                          "Id": mocked_instance_ids[0],
                                          "Port": 80
                                      },
                                      {
                                          "Id": mocked_instance_ids[1],
                                          "Port": 80
                                      },
                                  ])


def test_get_instances(ec2_client, elbv2_client, mocked_alb,
                       mocked_instance_ids):
    instance_ids = ALB().get_instance_ids(ALB_NAME)

    assert len(instance_ids) == 2
    assert mocked_instance_ids[0] == instance_ids[0]
    assert mocked_instance_ids[1] == instance_ids[1]
