import pytest

from esu.base import NotFoundEx
from esu.router import Router
from esu.router_port_forwarding import RouterPortForwarding
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_pf = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        RouterPortForwarding.get_object(router, router_pf)


@load_fixtures
def test_get_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_pf_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_pf = RouterPortForwarding.get_object(router, router_pf_id)

    assert isinstance(router_pf, RouterPortForwarding)
    assert router_pf.protocol == "tcp"
    assert router_pf.external_port_range_end == 80
    assert router_pf.external_port_range_start == 80
    assert router_pf.internal_port == 80
    assert router_pf.local_ip == "10.0.1.2"


@load_fixtures
def test_create(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_pf = RouterPortForwarding(protocol="tcp", local_ip="10.0.1.2",
                                     external_port_range_end=80,
                                     external_port_range_start=80,
                                     internal_port=80, router=router)
    router_pf.create()

    assert router_pf.id
    assert router_pf.protocol == "tcp"
    assert router_pf.external_port_range_end == 80
    assert router_pf.external_port_range_start == 80
    assert router_pf.internal_port == 80
    assert router_pf.local_ip == "10.0.1.2"


@load_fixtures
def test_reconfig(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_pf = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_pf = RouterPortForwarding.get_object(router=router, pf_id=router_pf)

    router_pf.protocol = "udp"
    router_pf.external_port_range_end = 100
    router_pf.external_port_range_start = 80
    router_pf.internal_port = 90
    router_pf.local_ip = "10.0.1.3"
    router_pf.save()

    assert router_pf.protocol == "udp"
    assert router_pf.external_port_range_end == 100
    assert router_pf.external_port_range_start == 80
    assert router_pf.internal_port == 90
    assert router_pf.local_ip == "10.0.1.3"


@load_fixtures
def test_destroy(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_pf = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_pf = RouterPortForwarding.get_object(router=router, pf_id=router_pf)
    router_pf.destroy()
