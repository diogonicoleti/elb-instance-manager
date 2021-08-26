from core.alb import ALB
from tests.helpers import assert_ec2_instance
from tests import ALB_NAME


def test_get_instances(ec2_client, elbv2_client, mocked_alb,
                       mocked_instance_ids):
    instance_ids = ALB().get_instance_ids(ALB_NAME)

    assert len(instance_ids) == 2
    assert mocked_instance_ids[0] == instance_ids[0]
    assert mocked_instance_ids[1] == instance_ids[1]


def test_register(elbv2_client, mocked_alb, mocked_instance_ids):
    registered_instance_id = mocked_instance_ids[2]
    alb = ALB()
    alb.register(ALB_NAME, registered_instance_id)

    instance_ids = alb.get_instance_ids(ALB_NAME)
    assert len(instance_ids) == 3
    assert registered_instance_id in instance_ids


def test_deregister(elbv2_client, mocked_alb, mocked_instance_ids):
    deregistered_instance_id = mocked_instance_ids[0]
    alb = ALB()
    alb.deregister(ALB_NAME, deregistered_instance_id)

    instance_ids = alb.get_instance_ids(ALB_NAME)
    assert len(instance_ids) == 1
    assert deregistered_instance_id not in instance_ids
