import pytest

from esu.firewall_template import FirewallTemplate
from esu.firewall_template_rule import FirewallTemplateRule
from esu.tests import load_fixtures


@load_fixtures
def test_get_by_id(rsps):
    firewall_template_id = '00000000-0000-0000-0000-000000000000'
    firewall_template = FirewallTemplate.get_object(id=firewall_template_id)

    assert isinstance(firewall_template, FirewallTemplate)
    assert firewall_template.id == firewall_template_id
    assert firewall_template.name == 'По-умолчанию'


@load_fixtures
def test_get_firewall_rules(rsps):
    firewall_template_id = '00000000-0000-0000-0000-000000000000'
    firewall_template = FirewallTemplate.get_object(id=firewall_template_id)
    rules = firewall_template.get_firewall_rules()

    assert len(rules) == 1
    rule = rules[0]
    assert isinstance(rule, FirewallTemplateRule)
    assert rule.id == '4bd4829d-b8c9-41cc-a02a-505dc0bc0c27'
    assert rule.direction == 'ingress'
    assert rule.name == 'Разрешить порт 10050'
    assert rule.dst_port_range_min == 10050
    assert rule.dst_port_range_max == None
    assert rule.destination_ip == "0.0.0.0/0"
    assert rule.protocol == "tcp"
