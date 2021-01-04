import pytest

from esu.base import NotFoundEx
from esu.template import Template
from esu.template_field import TemplateField
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    template_id = '40000000-4000-4000-4000-400000000000'
    with pytest.raises(NotFoundEx):
        Template.get_object(template_id)


@load_fixtures
def test_get_by_id(rsps):
    template_id = '70722cb1-6e03-4900-ad78-b680205cd002'
    template = Template.get_object(template_id)

    assert isinstance(template, Template)
    assert template.id == template_id
    assert template.name == 'VMWARE Ubuntu 16.04'


@load_fixtures
def test_get_fields(rsps):
    template_id = '70722cb1-6e03-4900-ad78-b680205cd002'
    template = Template.get_object(template_id)

    assert len(template.get_fields()) == 1
    field = template.get_fields()[0]
    assert isinstance(field, TemplateField)

    assert field.id == '70722cb1-6e03-4900-ad78-b680205ff002'
    assert field.name == 'Password'
    assert field.required is True
    assert field.system_alias == 'password'


@load_fixtures
def test_get_field(rsps):
    template_id = '70722cb1-6e03-4900-ad78-b680205cd002'
    template = Template.get_object(template_id)

    field = next(f for f in template.get_fields() \
        if f.system_alias == 'password')
    assert isinstance(field, TemplateField)
    assert field.id == '70722cb1-6e03-4900-ad78-b680205ff002'
