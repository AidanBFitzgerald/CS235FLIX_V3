import pytest
import os
from flix.adapters import memory_repository
from flix.adapters.memory_repository import MemoryRepository, populate


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data')
    populate(filename, repo)
    return repo
