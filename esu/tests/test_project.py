import pytest

from esu.base import NotFoundEx
from esu.client import Client
from esu.project import Project
from esu.tests import load_fixtures
from esu.vdc import Vdc


@load_fixtures
def test_not_found_by_id(rsps):
    project_id = '20000000-2000-2000-2000-200000000000'
    with pytest.raises(NotFoundEx):
        Project.get_object(project_id)


@load_fixtures
def test_get_by_id(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)

    assert isinstance(project, Project)
    assert project.id == project_id
    assert project.name == 'Project 1'


@load_fixtures
def test_get_client(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)
    client = project.client

    assert isinstance(client, Client)
    assert client.name == 'default'


@load_fixtures
def test_create(rsps):
    client_id = 'd5cd2cdc-b5b0-4d2e-8bc6-ea3f019745f9'
    client = Client.get_object(client_id)

    project = Project(name='Brand New Project', client=client)
    project.create()

    assert b'Brand New Project' in rsps.calls[1].request.body

    assert project.id
    assert project.name == 'Brand New Project'
    assert project.client.id == client.id


@load_fixtures
def test_rename(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)

    project.name = 'Project New Name'
    project.save()

    assert project.name == 'Project New Name'


@load_fixtures
def test_delete(rsps):
    project = Project(id='98bfb2e6-fb53-4371-945e-e83402b6d78f')
    project.destroy()

    assert project.id is None
    assert rsps.calls[0].request.method == 'DELETE'


@load_fixtures
def test_get_vdcs(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)

    vdcs = project.get_vdcs()
    assert len(vdcs) == 2
    assert isinstance(vdcs[0], Vdc)
    assert vdcs[0].name == 'kvm'
    assert vdcs[1].name == 'vmWare'
