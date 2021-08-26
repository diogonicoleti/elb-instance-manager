import pytest

from elb_instance_manager.core.ec2 import EC2
from tests.helpers import assert_ec2_instance
from tests import EXAMPLE_AMI_ID


@pytest.fixture
def mocked_instance_ids(ec2_client):
    reservation = ec2_client.run_instances(ImageId=EXAMPLE_AMI_ID,
                                           InstanceType='t3.micro',
                                           MaxCount=5,
                                           MinCount=5)
    return [instance['InstanceId'] for instance in reservation['Instances']]


def test_get_instances(ec2_client, mocked_instance_ids):
    instances = EC2().get_instances(mocked_instance_ids[:2])

    assert len(instances) == 2
    assert_ec2_instance(instances[0])
    assert_ec2_instance(instances[1])


def test_get_instance(ec2_client, mocked_instance_ids):
    instance = EC2().get_instance(mocked_instance_ids[0])
    assert_ec2_instance(instance)
