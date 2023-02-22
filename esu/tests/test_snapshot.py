from esu.snapshot import Snapshot
from esu.tests import load_fixtures
from esu.vm import Vm


@load_fixtures
def test_create(resp):
    vm_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    vm = Vm.get_object(vm_id)
    snapshot = Snapshot(name='test', description='test', vm=vm)
    snapshot.create()

    assert snapshot.vm.id == vm.id
    assert snapshot.name == 'test'


@load_fixtures
def test_get(resp):
    snapshot = Snapshot().get_object(id='3fa85f64-5717-4562-b3fc-2c963f66afa6')
    assert snapshot.vm.id == "3f69273f-1d77-4ef7-af31-c93221335014"
    assert snapshot.name == 'test'


@load_fixtures
def test_delete(resp):
    snapshot = Snapshot().get_object(id='3fa85f64-5717-4562-b3fc-2c963f66afa6')
    snapshot.destroy()
