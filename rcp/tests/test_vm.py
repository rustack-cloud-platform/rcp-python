import pytest

from rcp.base import NotFoundEx
from rcp.disk import Disk
from rcp.firewall_template import FirewallTemplate
from rcp.image import Image
from rcp.network import Network
from rcp.port import Port
from rcp.storage_profile import StorageProfile
from rcp.template import Template
from rcp.template_field import TemplateField
from rcp.tests import load_fixtures
from rcp.vdc import Vdc
from rcp.vm import Vm


@load_fixtures
def test_not_found_by_id(rsps):
    vm_id = '50000000-5000-5000-5000-500000000000'
    with pytest.raises(NotFoundEx):
        Vm.get_object(vm_id)


@load_fixtures
def test_get_by_id(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    assert isinstance(vm, Vm)
    assert vm.id == vm_id
    assert vm.name == 'vm1'
    assert vm.template.name == 'VMWARE Ubuntu 18'


@load_fixtures
def test_get_vm(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)
    vdc = vm.vdc

    assert isinstance(vdc, Vdc)
    assert vdc.name == 'Vdc New Name'


@load_fixtures
def test_create(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)
    template = Template.get_object('70722cb1-6e03-4900-ad78-b680205cd002')
    storage_profile = StorageProfile.get_object(
        '563a9b7c-419a-4630-9ac8-8022d740f12a')
    network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')
    disk_1 = Disk(storage_profile=storage_profile, name='Main disk #1',
                  size=10)
    disk_2 = Disk(storage_profile=storage_profile, name='Second disk #2',
                  size=12)

    firewall_template = next(f for f in vdc.get_firewall_templates() \
        if f.name == 'По-умолчанию')
    ports = [Port(network=network, fw_templates=[firewall_template])]

    password_field = next(f for f in template.get_fields() \
        if f.system_alias == 'password')
    metadata = [{'field': password_field, 'value': 'On3_tw0_thReE'}]

    vm = Vm(name='My New Vm', vdc=vdc, cpu=2, ram=4, template=template,
            ports=ports, disks=[disk_1, disk_2], metadata=metadata)

    assert vm.template.id == template.id
    assert len(vm.ports) == 1
    assert isinstance(vm.ports[0].network, Network)
    assert len(vm.disks) == 2
    assert isinstance(vm.disks[0], Disk)

    vm.create()

    assert vm.template.id == template.id
    assert len(vm.ports) == 1
    assert isinstance(vm.ports[0].network, Network)
    assert len(vm.ports[0].fw_templates) == 1
    assert vm.ports[0].fw_templates[
        0].id == '00000000-0000-0000-0000-000000000000'

    assert len(vm.disks) == 2
    assert isinstance(vm.disks[0], Disk)

    assert vm.id
    assert vm.name == 'My New Vm'
    assert vm.vdc.id == vdc.id
    assert vm.floating is None


@load_fixtures
def test_create_with_fip(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)
    template = Template.get_object('70722cb1-6e03-4900-ad78-b680205cd002')
    storage_profile = StorageProfile.get_object(
        '563a9b7c-419a-4630-9ac8-8022d740f12a')
    network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')
    disk_1 = Disk(storage_profile=storage_profile, name='Root disk', size=10)

    password_field = next(f for f in template.get_fields() \
        if f.system_alias == 'password')

    vm = Vm(name='My New Vm 2', vdc=vdc, cpu=1, ram=2, template=template,
            ports=[Port(network=network)], disks=[disk_1], metadata=[{
                'field': password_field,
                'value': 'On3_tw0_thReE'
            }], floating=Port())
    vm.create()

    assert vm.floating.ip_address == '74.53.11.5'


@load_fixtures
def test_create_with_ids_instead_of_objects(rsps):
    storage_profile = StorageProfile.get_object(
        '563a9b7c-419a-4630-9ac8-8022d740f12a')
    network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')
    disk_1 = Disk(storage_profile=storage_profile, name='Main disk #1',
                  size=10)  # existing disk
    disk_2 = Disk(storage_profile=storage_profile, name='Second disk #2',
                  size=12)

    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    template_id = '70722cb1-6e03-4900-ad78-b680205cd002'
    field = TemplateField(id='70722cb1-6e03-4900-ad78-b680205ff002')

    ports = [
        Port(
            network=network.id, fw_templates=[
                FirewallTemplate.get_object(
                    '00000000-0000-0000-0000-000000000000')
            ])
    ]

    metadata = [{'field': field, 'value': 'On3_tw0_thReE'}]

    vm = Vm(name='My New Vm', vdc=vdc_id, cpu=2, ram=4, template=template_id,
            ports=ports, disks=[disk_1, disk_2], metadata=metadata)

    assert vm.template.id == template_id
    assert len(vm.ports) == 1
    assert isinstance(vm.ports[0].network, Network)
    assert len(vm.disks) == 2
    assert isinstance(vm.disks[0], Disk)

    vm.create()

    assert vm.template.id == template_id
    assert len(vm.ports) == 1
    assert isinstance(vm.ports[0].network, Network)
    assert len(vm.disks) == 2
    assert isinstance(vm.disks[0], Disk)

    assert vm.id
    assert vm.name == 'My New Vm'
    assert vm.vdc.id == vdc_id


@load_fixtures
def test_add_disk(rsps):
    vm_id = 'b795bc88-5b9c-49b7-bed6-91669794bfda'
    vm = Vm.get_object(vm_id)

    assert isinstance(vm, Vm)
    assert len(vm.disks) == 1
    assert vm.disks[0].scsi == '0:0'

    disk = Disk(storage_profile='563a9b7c-419a-4630-9ac8-8022d740f12a',
                name='Second disk', size=12)

    assert disk.scsi is None  # Because it's a new disk
    vm.add_disk(disk)
    assert len(vm.disks) == 2
    assert vm.disks[1].scsi == '0:1'
    assert disk.scsi == '0:1'


@load_fixtures
def test_detach_disk(rsps):
    vm_id = '33d9d1af-cf31-4b55-aa44-590d020ab13a'
    vm = Vm.get_object(vm_id)

    assert isinstance(vm, Vm)
    assert len(vm.disks) == 2

    target_disk = vm.disks[1]
    assert target_disk.scsi == '0:1'
    assert target_disk.vm == vm

    vm.detach_disk(target_disk)
    assert target_disk.vm is None
    assert len(vm.disks) == 1


@load_fixtures
def test_rename(rsps):
    vm_id = '33d9d1af-cf31-4b55-aa44-590d020ab13a'
    vm = Vm.get_object(vm_id)

    vm.name = 'New VM Name 123'
    vm.save()

    assert vm.name == 'New VM Name 123'


@load_fixtures
def test_poweron(rsps):
    vm_id = '33d9d1af-cf31-4b55-aa44-590d020ab13a'
    vm = Vm.get_object(vm_id)

    assert vm.power is False
    vm.power_on()
    assert vm.power is True


@load_fixtures
def test_delete(rsps):
    vm = Vm(id='954fd467-fd9a-4ce7-b4df-1e81e557bce9')
    vm.destroy()

    assert vm.id is None
    assert rsps.calls[0].request.method == 'DELETE'


@load_fixtures
def test_get_ports(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    ports = vm.ports
    assert len(ports) == 1
    assert isinstance(ports[0], Port)


@load_fixtures
def test_get_disks(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    disks = vm.disks
    assert len(disks) == 1
    assert isinstance(disks[0], Disk)
    assert disks[0].size == 11


@load_fixtures
def test_mount_iso(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)
    image_id = 'f01776bb-968b-4b8f-835c-669535a9d0eb'
    image = Image.get_object(image_id)

    vm.mount_iso(image)


@load_fixtures
def test_unmount_iso(rsps):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)

    vm.unmount_iso()
