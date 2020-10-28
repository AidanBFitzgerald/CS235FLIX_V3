import pytest
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from werkzeug.security import generate_password_hash

from flix import create_app
import flix.adapters.repository as repo1
from flix.adapters import database_repository
from flix.adapters.memory_repository import MemoryRepository, populate
from flix.adapters.orm import metadata, map_model_to_tables
from flix.domain.model import User

TEST_DATA_PATH_MEMORY = os.path.join('tests', 'data')
TEST_DATA_PATH_DATABASE = os.path.join('tests', 'data', 'database')

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///CS235FLIX-test.db'


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data')
    populate(filename, repo)
    repo.add_user(User("shaun", '12345'))
    return repo


@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def empty_session():
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()


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
