import os

from flask import Flask

import flix.adapters.repository as repo
from flix.adapters.memory_repository import MemoryRepository, populate


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = os.path.join('flix', 'adapters', 'data')
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)
