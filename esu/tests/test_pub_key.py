from esu.public_key import PublicKey
from esu.tests import load_fixtures
from esu.user import User


@load_fixtures
def test_create(rsps):
    user_id = '5fbd6cf8-b346-434f-8192-884fb36f3c2c'
    user = User.get_object(user_id)
    key = PublicKey(name='test', public_key='1241ndJSDfjnk235125jk1')
    key.create(user)

    assert isinstance(key, PublicKey)
    assert key.name == 'test'
    assert key.public_key == '1241ndJSDfjnk235125jk1'


@load_fixtures
def test_delete(rsps):
    user_id = '5fbd6cf8-b346-434f-8192-884fb36f3c2c'
    user = User.get_object(user_id)
    key = PublicKey(id='e2fe4a85-16b1-4eac-a9a6-4c360caf1e3c')
    key.destroy(user)

    assert key.id is None
