import pytest

from rcp.base import NotFoundEx
from rcp.port import Port
from rcp.port_forwarding import PortForwarding
from rcp.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    port_forwarding = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        PortForwarding.get_object(port_forwarding)


@load_fixtures
def test_get_by_id(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)

    assert isinstance(port_forwarding, PortForwarding)
    assert port_forwarding.name == "10.11.143.46"
    assert port_forwarding.floating.id == "e53ac707-adb9-4426-bcc1"
    assert port_forwarding.floating.ip_address == "10.11.143.46"


@load_fixtures
def test_create(rsps):
    port_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    port = Port.get_object(port_id)
    p_f = PortForwarding(floating=port)
    p_f.create()

    assert p_f.id
    assert p_f.name == "10.11.143.46"
    assert p_f.floating.id == "954fd467-fd9a-4ce7-b4df-1e81e557bce9"
    assert p_f.floating.ip_address == "10.11.143.46"


@load_fixtures
def test_destroy(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    port_forwarding.destroy()
