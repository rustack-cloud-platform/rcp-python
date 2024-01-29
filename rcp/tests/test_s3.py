import pytest

from rcp.base import NotFoundEx
from rcp.api.project import Project
from rcp.s3 import S3
from rcp.tests import load_fixtures


# pylint: disable=invalid-name
@load_fixtures
def test_not_found_by_id(rsps):
    s3 = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        S3.get_object(s3)


@load_fixtures
def test_get_by_id(resp):
    s3 = S3().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert s3.id == 'f01776bb-968b-4b8f-835c-669535a9d0eb'
    assert s3.name == 'S3'


@load_fixtures
def test_create(rsps):
    project_id = 'a737cd39-e7a7-46b8-a756-fb8ccceeed8f'
    project = Project.get_object(project_id)

    s3 = S3(name='New S3', project=project)
    s3.create()

    assert s3.id
    assert s3.name == 'New S3'
    assert s3.project.id == project.id


@load_fixtures
def test_rename(rsps):
    s3 = S3.get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert s3.name == 'S3'

    s3.name = 'Renamed S3'
    s3.save()

    assert s3.name == 'Renamed S3'


@load_fixtures
def test_delete(rsps):
    s3 = S3.get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    assert s3.name == 'S3'
    s3.destroy()
