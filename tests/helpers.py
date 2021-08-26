from tests import INSTANCE_TYPE


def assert_ec2_instance(instance):
    assert instance['InstanceType'] == INSTANCE_TYPE
    assert instance['InstanceId'] is not None
    assert instance['LaunchTime'] is not None


def assert_machine_info(info):
    assert info['instanceType'] == INSTANCE_TYPE
    assert info['instanceId'] is not None
    assert info['launchDate'] is not None
