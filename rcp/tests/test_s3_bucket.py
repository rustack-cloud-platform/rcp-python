import pytest

from rcp.base import NotFoundEx
from rcp.s3 import S3
from rcp.s3_bucket import S3Bucket
from rcp.tests import load_fixtures


# pylint: disable=invalid-name
@load_fixtures
def test_not_found_by_id(rsps):
    s3 = S3().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    s3bucket = '21000000-2100-2100-2100-210000000000'

    with pytest.raises(NotFoundEx):
        S3Bucket.get_object(s3bucket, s3)


@load_fixtures
def test_get_by_id(resp):
    s3 = S3().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    s3bucket = S3Bucket.get_object('bef66c58-66d0-4161-a6ac-6caf85a9087d', s3)
    assert s3bucket.id == 'bef66c58-66d0-4161-a6ac-6caf85a9087d'
    assert s3bucket.name == 'S3bucket'


@load_fixtures
def test_create(rsps):
    s3 = S3().get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')

    s3bucket = S3Bucket(name='S3bucket')
    s3bucket.create(s3=s3)

    assert s3bucket.id
    assert s3bucket.name == 'S3bucket'


@load_fixtures
def test_rename(rsps):
    s3 = S3.get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    s3bucket = S3Bucket.get_object('bef66c58-66d0-4161-a6ac-6caf85a9087d', s3)
    assert s3bucket.name == 'S3bucket'

    s3bucket.name = 'Renamed S3bucket'
    s3bucket.save(s3=s3)

    assert s3bucket.name == 'Renamed S3bucket'


@load_fixtures
def test_delete(rsps):
    s3 = S3.get_object(id='f01776bb-968b-4b8f-835c-669535a9d0eb')
    s3bucket = S3Bucket.get_object('bef66c58-66d0-4161-a6ac-6caf85a9087d', s3)
    assert s3bucket.name == 'S3bucket'
    s3bucket.destroy(s3=s3)
