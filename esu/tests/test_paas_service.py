from esu.manager import Manager
from esu.paas_service import PaasService
from esu.tests import load_fixtures


@load_fixtures
def test_get_by_id(rsps):
    service_id = '7b5ff7fd-998b-404a-87f0-2ef788a2308d'
    service = PaasService.get_object(service_id)
    assert isinstance(service, PaasService)
    assert service.id == service_id
    assert service.name == 'Test PAAS service'


@load_fixtures
def test_get_all(rsps):
    service_id = '7b5ff7fd-998b-404a-87f0-2ef788a2308d'
    manager = Manager()
    services = manager.get_all_paas_services()
    assert len(services) == 1
    service = services[0]
    assert isinstance(service, PaasService)
    assert service.id == service_id
    assert service.name == 'Test PAAS service'
