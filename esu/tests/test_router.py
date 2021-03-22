import pytest

from esu import Port
from esu.base import NotFoundEx
from esu.router import Router
from esu.tests import load_fixtures
from esu.vdc import Vdc


@load_fixtures
def test_not_found_by_id(rsps):
    router = '11000000-1100-1100-1100-110000000000'
    with pytest.raises(NotFoundEx):
        Router.get_object(router)


@load_fixtures
def test_get_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)

    assert isinstance(router, Router)
    assert router.id == router_id
    assert router.name == 'Default'
    assert len(router.ports) == 2
    assert router.ports[0].network.id == '9c7d5517-e920-4df0-aced-0146c3f67ff8'
    assert router.ports[1].network.id == '09110dd6-2868-40f7-9aca-e4cda281ad0d'
    assert len(router.ports) == 2
    assert isinstance(router.floating, Port)
    assert router.floating.ip_address == '74.53.11.2'


@load_fixtures
def test_create(rsps):
    vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
    vdc = Vdc.get_object(vdc_id)

    network_id = '9c7d5517-e920-4df0-aced-0146c3f67ff8'
    router = Router(name='New router', vdc=vdc,
                    ports=[Port(network=network_id)])
    router.create()

    assert router.id
    assert router.name == 'New router'
    assert router.vdc.id == vdc.id
    assert router.floating is None


@load_fixtures
def test_create_with_fip(rsps):
    vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
    vdc = Vdc.get_object(vdc_id)

    network_id = '9c7d5517-e920-4df0-aced-0146c3f67ff8'
    router = Router(name='New router with fip', vdc=vdc,
                    ports=[Port(network=network_id)], floating=Port())
    router.create()

    assert router.name == 'New router with fip'
    assert router.floating.ip_address == '74.53.11.4'


@load_fixtures
def test_rename(rsps):
    router = Router.get_object('58385696-32c6-4a5c-bafe-895815eedf04')
    assert router.name == 'Default'

    router.name = 'Renamed default router'
    router.save()

    assert router.name == 'Renamed default router'


@load_fixtures
def test_delete(rsps):
    router = Router.get_object('300052f3-00a8-4f86-9211-7ca830dff76a')
    router.destroy()
