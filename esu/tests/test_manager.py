from esu.client import Client
from esu.manager import Manager
from esu.project import Project
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
