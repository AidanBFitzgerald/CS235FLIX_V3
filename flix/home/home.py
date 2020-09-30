from flask import Blueprint

home_blueprint = Blueprint('home.bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    pass
