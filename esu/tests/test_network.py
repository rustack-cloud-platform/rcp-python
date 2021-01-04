import pytest

from esu.base import NotFoundEx
from esu.network import Network
from esu.subnet import Subnet
from esu.tests import load_fixtures
from esu.vdc import Vdc


@load_fixtures
def test_not_found_by_id(rsps):
    network = '80000000-8000-8000-8000-800000000000'
    with pytest.raises(NotFoundEx):
        Network.get_object(network)


@load_fixtures
def test_get_by_id(rsps):
    network_id = 'b9e6df93-0d04-4dac-a3c1-1a8539b8e445'
    network = Network.get_object(network_id)

    assert isinstance(network, Network)
    assert network.id == network_id
    assert network.name == 'Default'
    assert len(network.subnets) == 2
    assert network.subnets[0].cidr == '10.0.1.0/24'
    assert network.subnets[1].cidr == '10.22.23.0/24'


@load_fixtures
def test_create(rsps):
    vdc_id = 'e5d9a192-c5da-485a-b134-1b14ec9c57d9'
    vdc = Vdc.get_object(vdc_id)

    network = Network(name='Brand New Network', vdc=vdc)
    network.create()

    assert network.id
    assert network.name == 'Brand New Network'
    assert network.vdc.id == vdc.id


@load_fixtures
def t_est_create_with_subnet(rsps):
    vdc_id = '70eb1ec5-3e54-4df8-a096-ec26526ec89b'
    vdc = Vdc.get_object(vdc_id)

    subnet = Subnet(cidr='10.49.1.0/24', gateway='10.49.1.1',
                    start_ip='10.49.1.2', end_ip='10.49.1.254',
                    enable_dhcp=True)

    network = Network(name='Brand New Network with subnet', vdc=vdc,
                      subnets=[subnet])
    network.create()

    assert len(network.subnets) == 1
    # assert network.name == 'Brand New Network'
    # assert network.vdc.id == vdc.id


@load_fixtures
def test_rename(rsps):
    network = Network.get_object('0b594d5a-1e24-484e-b624-9e139942e2f3')
    assert network.name == 'Custom network'

    network.name = 'Net1'
    network.save()

    assert network.name == 'Net1'


@load_fixtures
def test_add_subnet(rsps):
    network = Network.get_object('b9e6df93-0d04-4dac-a3c1-1a8539b8e445')

    subnet = Subnet(cidr='10.22.23.0/24', gateway='10.22.23.1',
                    start_ip='10.22.23.2', end_ip='10.22.23.254',
                    enable_dhcp=True)

    assert len(network.subnets) == 2
    network.add_subnet(subnet)
    assert len(network.subnets) == 3


@load_fixtures
def test_remove_subnet(rsps):
    network = Network.get_object('b2d48cbc-5902-4512-b47d-5a858935e832')

    assert len(network.subnets) == 1
    assert network.subnets[0].id == 'cb2de3aa-2083-4864-b753-9f75c642da71'
    network.remove_subnet(network.subnets[0])
    assert len(network.subnets) == 0


@load_fixtures
def test_delete(rsps):
    network = Network.get_object('0b594d5a-1e24-484e-b624-9e139942e2f3')
    network.destroy()
