import pytest

from flix.adapters import memory_repository
from flix.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate('data/', repo)
    return repo
