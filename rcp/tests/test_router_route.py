import pytest

from rcp.base import NotFoundEx
from rcp.router import Router
from rcp.router_route import RouterRoute
from rcp.tests import load_fixtures


@load_fixtures
def test_not_found_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_route = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        RouterRoute.get_object(router, router_route)


@load_fixtures
def test_get_by_id(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_route_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_route = RouterRoute.get_object(router, router_route_id)

    assert isinstance(router_route, RouterRoute)
    assert router_route.destination == "10.0.2.0/24"
    assert router_route.nexthop == "10.0.1.1"


@load_fixtures
def test_create(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_route = RouterRoute(router=router, destination="10.0.2.0/24",
                               nexthop="10.0.1.1")
    router_route.create()

    assert router_route.id
    assert router_route.destination == "10.0.2.0/24"
    assert router_route.nexthop == "10.0.1.1"


@load_fixtures
def test_update(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_route_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_route = RouterRoute.get_object(router, router_route_id)

    router_route.destination = "10.0.3.0/24"
    router_route.nexthop = "10.0.1.3"
    router_route.save()

    assert router_route.destination == "10.0.3.0/24"
    assert router_route.nexthop == "10.0.1.3"


@load_fixtures
def test_destroy(rsps):
    router_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router = Router.get_object(router_id)
    router_route_id = '58385696-32c6-4a5c-bafe-895815eedf04'
    router_route = RouterRoute.get_object(router, router_route_id)

    router_route.destroy()
