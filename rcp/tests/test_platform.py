from rcp.platform import Platform
from rcp.tests import load_fixtures


@load_fixtures
def test_get_by_id(rsps):
    platform_id = 'ace18e86-9fba-4a50-845b-b36e677b2a3f'
    hypervisor_id = '478f179a-037a-4795-a8c4-7cf0a83b5390'
    platform = Platform.get_object(platform_id)
    assert isinstance(platform, Platform)
    assert platform.id == platform_id
    assert platform.name == 'Intel Cascade Lake'
    assert platform.hypervisor.id == hypervisor_id
    assert platform.hypervisor.name == 'vmware'
