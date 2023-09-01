from esu.client import Client
from esu.firewall_template import FirewallTemplate
from esu.manager import Manager
from esu.network import Network
from esu.platform import Platform
from esu.project import Project
from esu.storage_profile import StorageProfile
from esu.tests import load_fixtures
from esu.vdc import Vdc
from esu.vm import Vm


@load_fixtures
def test_get_all_clients(rsps):
    manager = Manager()
    clients = manager.get_all_clients()
    assert len(clients) == 2
    assert isinstance(clients[0], Client)
    assert clients[0].name == 'Client 2'


@load_fixtures
def test_get_all_projects(rsps):
    manager = Manager()
    projects = manager.get_all_projects()
    assert len(projects) == 3
    assert isinstance(projects[0], Project)
    assert projects[0].name == 'Empty Project'


@load_fixtures
def test_get_all_vdcs(rsps):
    manager = Manager()
    vdcs = manager.get_all_vdcs()
    assert len(vdcs) == 3
    assert isinstance(vdcs[0], Vdc)
    assert vdcs[0].name == 'kvm'


@load_fixtures
def test_get_all_vms(rsps):
    manager = Manager()
    vms = manager.get_all_vms()
    assert len(vms) == 21
    assert isinstance(vms[0], Vm)
    assert vms[0].name == 'vm_015'


@load_fixtures
def test_get_all_platforms(rsps):
    manager = Manager()
    platforms = manager.get_all_platforms()
    assert len(platforms) == 3
    assert isinstance(platforms[0], Platform)
    assert platforms[0].name == 'Базовая kvm'


@load_fixtures
def test_get_all_firewall_templates(rsps):
    manager = Manager()
    fw_templates = manager.get_all_firewall_templates()
    assert len(fw_templates) == 6
    assert isinstance(fw_templates[0], FirewallTemplate)
    assert fw_templates[0].name == 'Разрешить WEB'


@load_fixtures
def test_get_all_networks(rsps):
    manager = Manager()
    networks = manager.get_all_networks()
    assert len(networks) == 2
    assert isinstance(networks[0], Network)
    assert networks[0].name == 'Default'


@load_fixtures
def test_get_all_storage_profiles(rsps):
    manager = Manager()
    storage_profiles = manager.get_all_storage_profiles()
    assert len(storage_profiles) == 2
    assert isinstance(storage_profiles[0], StorageProfile)
    assert storage_profiles[0].name == 'SATA VMWARE'
