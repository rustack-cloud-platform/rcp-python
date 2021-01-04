import pytest

from esu.base import NotFoundEx
from esu.client import Client
from esu.project import Project
from esu.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    client_id = '10000000-1000-1000-1000-100000000000'
    with pytest.raises(NotFoundEx):
        Client.get_object(client_id)


@load_fixtures
def test_get_by_id(rsps):
    client_id = 'd5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9'
    client = Client.get_object(client_id)

    assert isinstance(client, Client)
    assert client.id == client_id
    assert client.name == 'default'
    assert client.balance == 2550.63
    assert client.payment_model == 'postpay'


@load_fixtures
def test_get_projects(rsps):
    client_id = 'd5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9'
    client = Client.get_object(client_id)

    projects = client.get_projects()
    assert len(projects) == 2
    assert isinstance(projects[0], Project)
    assert projects[0].name == 'Project 2'
