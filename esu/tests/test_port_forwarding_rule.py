import pytest

from esu.base import NotFoundEx
from esu.port import Port
from esu.port_forwarding import PortForwarding
from esu.port_forwarding_rule import PortForwardingRule
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    port_forwarding_rule = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        PortForwardingRule.get_object(port_forwarding, port_forwarding_rule)


@load_fixtures
def test_get_by_id(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    port_forwarding_rule = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding_rule = PortForwardingRule.get_object(
        port_forwarding, port_forwarding_rule)

    assert isinstance(port_forwarding_rule, PortForwardingRule)
    assert port_forwarding_rule.internal_port == 80
    assert port_forwarding_rule.external_port == 80
    assert port_forwarding_rule.protocol == "tcp"


@load_fixtures
def test_create(rsps):
    port_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    port = Port.get_object(port_id)
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    p_f_rule = PortForwardingRule(port_forwarding=port_forwarding,
                                  internal_port=80, external_port=80,
                                  protocol="tcp", port=port)
    p_f_rule.create()

    assert p_f_rule.id
    assert isinstance(p_f_rule.port, Port)
    assert p_f_rule.port.id == '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    assert p_f_rule.internal_port == 80
    assert p_f_rule.external_port == 80
    assert p_f_rule.protocol == "tcp"


@load_fixtures
def test_update(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    port_forwarding_rule = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding_rule = PortForwardingRule.get_object(
        port_forwarding, port_forwarding_rule)

    port_forwarding_rule.internal_port = 90
    port_forwarding_rule.external_port = 90
    port_forwarding_rule.protocol = "udp"
    port_forwarding_rule.save()


@load_fixtures
def test_destroy(rsps):
    port_forwarding_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding = PortForwarding.get_object(port_forwarding_id)
    port_forwarding_rule = '58385696-32c6-4a5c-bafe-895815eedf04'
    port_forwarding_rule = PortForwardingRule.get_object(
        port_forwarding, port_forwarding_rule)
    port_forwarding_rule.destroy()
