from elb_instance_manager.resources.health_check import HealthCheckResource


def test_get():
    body, http_status = HealthCheckResource().get()
    assert http_status == 200
    assert body == {'status': 'OK'}
