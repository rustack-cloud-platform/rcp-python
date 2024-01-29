import pytest

from rcp.backup import Backup, RestorePoint, VmInBackup
from rcp.base import NotFoundEx
from rcp.tests import load_fixtures
from rcp.vdc import Vdc
from rcp.vm import Vm


@load_fixtures
def test_not_found_by_id(rsps):
    backup = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        Backup.get_object(backup)


@load_fixtures
def test_get_by_id(resp):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')

    assert isinstance(backup, Backup)
    assert backup.id == 'f01776bb-968b-4b8f-835c-669535a9d0eb'
    assert backup.name == 'New_Backup'
    assert backup.time == '09:00:00'
    assert backup.week_days == [1]
    assert backup.size == 0.9108
    assert isinstance(backup.vms[0], VmInBackup)


@load_fixtures
def test_create(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vdc = Vdc.get_object(vdc_id)
    vm = Vm.get_object(vm_id)

    backup = Backup(name="Test_Backup", vdc=vdc, vms=[vm], week_days=[1, 2],
                    time="09:00:00", retain_cycles=2)
    backup.create()

    assert backup.id
    assert backup.name == "Test_Backup"
    assert backup.vdc.id == vdc_id
    assert backup.week_days == [1, 2]
    assert backup.retain_cycles == 2
    assert backup.time == "09:00:00"
    assert backup.vms[0].id == vm_id


@load_fixtures
def test_add_one_more_vm(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert backup.name == "New_Backup"

    backup.vms.append(vm)
    backup.save()

    assert len(backup.vms) == 2
    assert backup.vms[1].id == vm_id


@load_fixtures
def test_reconfig_backup(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert backup.name == "New_Backup"
    assert backup.retain_cycles == 14
    assert backup.week_days == [1]
    assert backup.time == "09:00:00"

    backup.name = "Backup_renamed"
    backup.time = "11:00:00"
    backup.retain_cycles = 2
    backup.week_days = [1, 2]
    backup.save()

    assert backup.name == "Backup_renamed"
    assert backup.retain_cycles == 2
    assert backup.week_days == [1, 2]
    assert backup.time == "11:00:00"


@load_fixtures
def test_start_immediately(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    backup.start_immediately()


@load_fixtures
def test_get_restore_points(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    result = backup.get_restore_points()

    assert len(result) == 1
    assert isinstance(result[0], RestorePoint)
    assert isinstance(result[0].vm, Vm)


@load_fixtures
def test_restore(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    rps = backup.get_restore_points()
    restore_point = rps[0]
    backup.restore(restore_point=restore_point)


@load_fixtures
def test_get_backup_logs(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    backup.get_backup_log()


@load_fixtures
def test_get_restore_logs(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)
    backup = Backup()
    backup.get_restore_log(vm=vm)


@load_fixtures
def test_delete(rsps):
    backup = Backup().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    backup.destroy()
