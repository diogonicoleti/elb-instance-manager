from resources.elb import ELBResource
from tests.helpers import assert_machine_info
from tests import ALB_NAME


def test_get(ec2_client, elbv2_client, mocked_alb):
    body, http_status = ELBResource().get(ALB_NAME)

    assert http_status == 200
    assert len(body) == 2
    assert_machine_info(body[0])
    assert_machine_info(body[1])
