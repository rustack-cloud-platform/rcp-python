from esu.network import Network
from esu.port import Port
from esu.tests import load_fixtures
from esu.vdc import Vdc
from esu.vm import Vm


@load_fixtures
def test_create_port(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    port = Port(network=network)
    port.create()

    assert isinstance(port, Port)
    assert port.network.id == network.id
    assert port.type == 'orphan_int'


@load_fixtures
def test_connect(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    device = Vm().get_object(id='17580bd1-b548-4214-8614-6cfee656bd6f')
    port = Port(network=network)
    port.create()
    port.device = device
    port.ip_address = '0.0.0.0'
    port.save()
    assert isinstance(port, Port)
    assert port.device.id == device.id
    assert port.network.id == network.id


@load_fixtures
def test_disconnect(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    device = Vm().get_object(id='17580bd1-b548-4214-8614-6cfee656bd6f')
    port = Port(network=network, device=device)
    port.create()

    assert isinstance(port, Port)
    assert port.device.id == device.id
    assert port.network.id == network.id
    port.disconnect()
    assert port.device is None


@load_fixtures
def test_get_by_id(rsps):
    port_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    port = Port.get_object(port_id)
    assert port.id == port_id


@load_fixtures
def test_delete_port(resp):
    port_id = '954fd467-fd9a-4ce7-b4df-1e81e557bce9'
    port = Port.get_object(port_id)
    assert port.id == port_id
    port.destroy()


@load_fixtures
def test_create_fip(resp):
    vdc = Vdc().get_object(id='e5d9a192-c5da-485a-b134-1b14ec9c57d9')
    port = Port(vdc=vdc)
    port.create_fip()
    assert port.type == 'orphan_ext'
