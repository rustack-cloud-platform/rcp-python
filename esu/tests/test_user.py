import pytest

from esu.base import NotFoundEx
from esu.tests import load_fixtures
from esu.user import User


@load_fixtures
def test_not_found_by_id(rsps):
    user = '21000000-2100-2100-2100-210000000000'
    with pytest.raises(NotFoundEx):
        User.get_object(user)


@load_fixtures
def test_get_by_me(rsps):
    user_id = 'me'
    user = User.get_object(user_id)

    assert isinstance(user, User)
    assert user.login == 'test_login'
    assert user.username == 'test_username'


@load_fixtures
def test_get_by_id(rsps):
    user_id = '5fbd6cf8-b346-434f-8192-884fb36f3c2c'
    user = User.get_object(user_id)

    assert isinstance(user, User)
    assert user.login == 'test_login'
    assert user.username == 'test_username'
