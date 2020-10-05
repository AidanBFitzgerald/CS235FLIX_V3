import pytest
import os
from flix.adapters import memory_repository
from flix.adapters.memory_repository import MemoryRepository, populate
from flix.domain.model import User


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data')
    populate(filename, repo)
    repo.add_user(User("shaun", '12345'))
    return repo
