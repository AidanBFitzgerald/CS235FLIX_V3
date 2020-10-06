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

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

    return app
