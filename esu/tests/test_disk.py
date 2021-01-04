import pytest

from esu.base import NotFoundEx
from esu.disk import Disk
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    disk = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        Disk.get_object(disk)


@load_fixtures
def test_get_by_id(rsps):
    disk_id = '5fbd6cf8-b346-434f-8192-884fb36f3c2c'
    disk = Disk.get_object(disk_id)

    assert isinstance(disk, Disk)
    assert disk.name == 'Disk 2'
    assert disk.size == 15


# @load_fixtures
# def test_create(rsps):
#     vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
#     vdc = Vdc.get_object(vdc_id)

#     network_id = '9c7d5517-e920-4df0-aced-0146c3f67ff8'
#     router = Router(name='New router', vdc=vdc,
#                     ports=[Port(network=network_id)])
#     router.create()

#     assert router.id
#     assert router.name == 'New router'
#     assert router.vdc.id == vdc.id
#     assert router.floating is None

# @load_fixtures
# def test_create_with_fip(rsps):
#     vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
#     vdc = Vdc.get_object(vdc_id)

#     network_id = '9c7d5517-e920-4df0-aced-0146c3f67ff8'
#     router = Router(name='New router with fip', vdc=vdc,
#                     ports=[Port(network=network_id)], floating=Port())
#     router.create()

#     assert router.name == 'New router with fip'
#     assert router.floating.ip_address == '74.53.11.3'


@load_fixtures
def test_rename(rsps):
    disk = Disk.get_object('5fbd6cf8-b346-434f-8192-884fb36f3c2c')
    disk.name = 'Disk 2 renamed'
    disk.save()

    assert disk.name == 'Disk 2 renamed'


@load_fixtures
def test_delete(rsps):
    disk = Disk.get_object('f8e4251f-6079-40a5-8e0d-fc7058e3842c')
    disk.destroy()
