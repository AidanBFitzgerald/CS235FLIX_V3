from flask import Blueprint, render_template
from flix.adapters import repository as repo
from flix.movies import services

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    watchlist = services.get_watchlist(repo.repo_instance)
    return render_template("home/home.html", watchlist=watchlist)
