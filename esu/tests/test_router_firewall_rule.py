import pytest

from esu.base import NotFoundEx
from esu.router import Router
from esu.router_firewall_rule import RouterFirewallRule
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_firewall_rule = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        RouterFirewallRule.get_object(router, router_firewall_rule)


@load_fixtures
def test_get_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    firewall_rule_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    firewall_rule = RouterFirewallRule.get_object(router, firewall_rule_id)

    assert isinstance(firewall_rule, RouterFirewallRule)
    assert firewall_rule.name == "New_router_firewall_rule"
    assert firewall_rule.protocol == "tcp"
    assert firewall_rule.direction == "ingress"
    assert firewall_rule.source_ip == "10.0.1.0/24"
    assert firewall_rule.src_port_range_min == 80
    assert firewall_rule.src_port_range_max == 90
    assert firewall_rule.destination_ip is None
    assert firewall_rule.dst_port_range_min == 80
    assert firewall_rule.dst_port_range_max == 90


@load_fixtures
def test_create(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    fw_rule = RouterFirewallRule(name="Rule", protocol="tcp", router=router,
                                 direction="ingress", source_ip="10.0.1.0/24",
                                 src_port_range_min=80, src_port_range_max=90,
                                 dst_port_range_min=80, dst_port_range_max=90)
    fw_rule.create()

    assert fw_rule.id
    assert fw_rule.name == "Rule"
    assert fw_rule.direction == "ingress"
    assert fw_rule.source_ip == "10.0.1.0/24"
    assert fw_rule.src_port_range_min == 80
    assert fw_rule.src_port_range_max == 90
    assert fw_rule.destination_ip is None
    assert fw_rule.dst_port_range_min == 80
    assert fw_rule.dst_port_range_max == 90


@load_fixtures
def test_reconfig(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    fw_rule_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    fw_rule = RouterFirewallRule.get_object(router=router, rule_id=fw_rule_id)

    fw_rule.name = "Rule Renamed"
    fw_rule.direction = "egress"
    fw_rule.source_ip = None
    fw_rule.src_port_range_min = None
    fw_rule.src_port_range_max = None
    fw_rule.destination_ip = "10.0.1.0/24"
    fw_rule.dst_port_range_min = 100
    fw_rule.dst_port_range_max = 200
    fw_rule.save()

    assert fw_rule.name == "Rule Renamed"
    assert fw_rule.direction == "egress"
    assert fw_rule.source_ip is None
    assert fw_rule.src_port_range_min is None
    assert fw_rule.src_port_range_max is None
    assert fw_rule.destination_ip == "10.0.1.0/24"
    assert fw_rule.dst_port_range_min == 100
    assert fw_rule.dst_port_range_max == 200


@load_fixtures
def test_destroy(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    fw_rule_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    fw_rule = RouterFirewallRule.get_object(router=router, rule_id=fw_rule_id)

    fw_rule.destroy()
