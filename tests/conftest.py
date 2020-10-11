import pytest
import os

from werkzeug.security import generate_password_hash

from flix import create_app
import flix.adapters.repository as repo1
from flix.adapters.memory_repository import MemoryRepository, populate
from flix.domain.model import User

TEST_DATA_PATH = os.path.join('tests', 'data')


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data')
    populate(filename, repo)
    repo.add_user(User("shaun", '12345'))
    return repo


@pytest.fixture
def client():
    my_app = create_app({'TESTING': True,  # Set to True during testing.
                         'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
                         'WTF_CSRF_ENABLED': False})
    repo1.repo_instance.add_user(User("shaun", generate_password_hash("12345")))
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='shaun', password='12345'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
