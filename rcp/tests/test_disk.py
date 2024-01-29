import pytest

from rcp.base import NotFoundEx
from rcp.disk import Disk
from rcp.tests import load_fixtures


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
