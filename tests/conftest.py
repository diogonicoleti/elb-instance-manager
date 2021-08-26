import boto3
import pytest
import os

from moto import mock_ec2, mock_elbv2
from tests import EXAMPLE_AMI_ID, ALB_NAME


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


@pytest.fixture(scope='function')
def ec2_client(aws_credentials):
    with mock_ec2():
        yield boto3.client("ec2", region_name="us-east-1")


@pytest.fixture(scope='function')
def elbv2_client(aws_credentials):
    with mock_elbv2():
        yield boto3.client("elbv2", region_name="us-east-1")


@pytest.fixture(scope='function')
def mocked_instance_ids(ec2_client):
    reservation = ec2_client.run_instances(ImageId=EXAMPLE_AMI_ID,
                                           InstanceType='t3.micro',
                                           MaxCount=5,
                                           MinCount=5)
    return [instance['InstanceId'] for instance in reservation['Instances']]


@pytest.fixture(scope='function')
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
