from rcp.kubernetes import Kubernetes
from rcp.tests import load_fixtures


@load_fixtures
def test_create(rsps):
    k8s = Kubernetes(
        name='test', vdc='e5d9a192-c5da-485a-b134-1b14ec9c57d9', node_cpu=2,
        node_ram=2, node_disk_size=10,
        node_storage_profile='563a9b7c-419a-4630-9ac8-8022d740f12a',
        nodes_count=2, user_public_key='e2fe4a85-16b1-4eac-a9a6-4c360caf1e3c',
        template='253a9d25-3191-43de-ab9e-d2fbd48982c2')
    k8s.create()

    assert isinstance(k8s, Kubernetes)
    assert k8s.name == 'test'
    assert k8s.vdc.id == 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    assert k8s.node_cpu == 2


@load_fixtures
def test_get(rsps):
    k8s = Kubernetes().get_object('eea40fd7-7f55-4be1-a6b2-c9517382bf24')
    assert isinstance(k8s, Kubernetes)
    assert k8s.name == 'test'
    assert k8s.id == 'eea40fd7-7f55-4be1-a6b2-c9517382bf24'
    assert k8s.node_cpu == 2


@load_fixtures
def test_delete(rsps):
    k8s = Kubernetes(id='eea40fd7-7f55-4be1-a6b2-c9517382bf24')
    k8s.destroy()
    assert k8s.id is None
