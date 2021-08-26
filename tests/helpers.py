
def assert_ec2_instance(instance):
    assert instance['InstanceType'] == 't3.micro'
    assert instance['InstanceId'] is not None
    assert instance['LaunchTime'] is not None
