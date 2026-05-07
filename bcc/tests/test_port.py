from bcc.network import Network
from bcc.port import Port
from bcc.tests import load_fixtures
from bcc.vdc import Vdc
from bcc.vm import Vm


@load_fixtures
def test_create_port_int(resp):
    network = Network().get_object(id='9c7d5517-e920-4df0-aced-0146c3f67ff8')
    port = Port(network=network)
    port.create()

    assert isinstance(port, Port)
    assert port.network.id == network.id
    assert port.type == 'orphan_int'


@load_fixtures
def test_create_port_int_with_vdc(resp):
    network = Network().get_object(id='9c7d5517-e920-4df0-aced-0146c3f67ff8')
    vdc = Vdc().get_object(id='70eb1ec5-3e54-4df8-a096-ec26526ec89b')
    port = Port(network=network, vdc=vdc)
    port.create()

    assert isinstance(port, Port)
    assert port.network.id == network.id
    assert port.vdc.id == vdc.id
    assert port.type == 'orphan_int'


@load_fixtures
def test_create_port_user_ext(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    port = Port(network=network)
    port.create()

    assert isinstance(port, Port)
    assert port.network.id == network.id
    assert port.type == 'orphan_user_ext'


@load_fixtures
def test_create_port_user_ext_with_vdc(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    vdc = Vdc().get_object(id='70eb1ec5-3e54-4df8-a096-ec26526ec89b')
    port = Port(network=network, vdc=vdc)
    port.create()

    assert isinstance(port, Port)
    assert port.network.id == network.id
    assert port.vdc.id == vdc.id
    assert port.type == 'orphan_user_ext'


@load_fixtures
def test_connect(resp):
    network = Network().get_object(id='09110dd6-2868-40f7-9aca-e4cda281ad0d')
    device = Vm().get_object(id='17580bd1-b548-4214-8614-6cfee656bd6f')
    port = Port(network=network)
    port.create()
    port.vm = device

    print(port.connected)
    port.connect()
    assert isinstance(port, Port)


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
