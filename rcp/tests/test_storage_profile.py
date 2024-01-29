import pytest

from rcp.base import NotFoundEx
from rcp.storage_profile import StorageProfile
from rcp.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    storage_profile_id = '70000000-7000-7000-7000-700000000000'
    with pytest.raises(NotFoundEx):
        StorageProfile.get_object(storage_profile_id)


@load_fixtures
def test_get_by_id(rsps):
    storage_profile_id = '563a9b7c-419a-4630-9ac8-8022d740f12a'
    storage_profile = StorageProfile.get_object(storage_profile_id)

    assert isinstance(storage_profile, StorageProfile)
    assert storage_profile.id == storage_profile_id
    assert storage_profile.name == 'SATA KVM'
