import pytest

from esu.base import NotFoundEx
from esu.disk import Disk
from esu.firewall_template import FirewallTemplate
from esu.network import Network
from esu.port import Port
from esu.project import Project
from esu.router import Router
from esu.storage_profile import StorageProfile
from esu.template import Template
from esu.tests import load_fixtures
from esu.vdc import Vdc
from esu.vm import Vm


@load_fixtures
def test_not_found_by_id(rsps):
    vdc_id = '30000000-3000-3000-3000-300000000000'
    with pytest.raises(NotFoundEx):
        Vdc.get_object(vdc_id)


@load_fixtures
def test_get_by_id(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    assert isinstance(vdc, Vdc)
    assert vdc.id == vdc_id
    assert vdc.name == 'vmWare'


@load_fixtures
def test_get_project(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)
    project = vdc.project

    assert isinstance(project, Project)
    assert project.name == 'Project New Name'


@load_fixtures
def test_create(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)

    hypervisor = next(h for h in project.get_available_hypervisors() \
        if h.type == 'kvm')

    vdc = Vdc(name='Brand New Vdc', project=project, hypervisor=hypervisor)
    vdc.create()

    assert b'Brand New Vdc' in rsps.calls[1].request.body

    assert vdc.id
    assert vdc.name == 'Brand New Vdc'
    assert vdc.project.id == project.id


@load_fixtures
def test_rename(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    vdc.name = 'Vdc New Name'
    vdc.save()

    assert vdc.name == 'Vdc New Name'


@load_fixtures
def test_delete(rsps):
    vdc = Vdc(id='fd20bb3b-b37c-4d77-8f3d-27c167b0d890')
    vdc.destroy()

    assert vdc.id is None
    assert rsps.calls[0].request.method == 'DELETE'


@load_fixtures
def test_get_vms(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    vms = vdc.get_vms()
    assert len(vms) == 3
    assert isinstance(vms[0], Vm)
    assert vms[0].name == 'vm3'


@load_fixtures
def test_get_templates(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    templates = vdc.get_templates()
    assert len(templates) == 16
    assert isinstance(templates[0], Template)
    assert templates[0].name == 'Ubuntu 18 (cloud)'


@load_fixtures
def test_get_many_vms(rsps):
    vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
    vdc = Vdc.get_object(vdc_id)

    vms = vdc.get_vms()
    assert len(vms) == 18


@load_fixtures
def test_get_storage_profiles(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    storage_profiles = vdc.get_storage_profiles()
    assert len(storage_profiles) == 1
    assert isinstance(storage_profiles[0], StorageProfile)
    assert storage_profiles[0].name == 'SATA VMWARE'


@load_fixtures
def test_get_get_firewall_templates(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    firewall_templates = vdc.get_firewall_templates()
    assert len(firewall_templates) == 7
    assert isinstance(firewall_templates[0], FirewallTemplate)
    assert firewall_templates[0].name == 'Разрешить WEB'


@load_fixtures
def test_get_networks(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    networks = vdc.get_networks()
    assert len(networks) == 1
    assert isinstance(networks[0], Network)
    assert networks[0].name == 'Default'


@load_fixtures
def test_get_routers(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    routers = vdc.get_routers()
    assert len(routers) == 1
    assert isinstance(routers[0], Router)
    assert routers[0].name == 'Router'


@load_fixtures
def test_get_ports(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    ports = vdc.get_ports()
    assert len(ports) == 7
    assert isinstance(ports[0], Port)
    assert ports[0].ip_address == '10.0.1.1'
    assert ports[0].type == 'router_int'


@load_fixtures
def test_get_disks(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    disks = vdc.get_disks()
    assert len(disks) == 7
    assert isinstance(disks[0], Disk)
    assert disks[0].scsi == '0:0'
