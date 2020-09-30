# Configure Blueprint
from flask import Blueprint, request

movies_blueprint = Blueprint('movies.bp', __name__)


@movies_blueprint.route('/movies_by_letter', methods=['GET'])
def movies_by_letter():
    target_letter = request.args.get('letter')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    pass


@movies_blueprint.route('search', methods=['GET', 'POST'])
def search():
    pass


@movies_blueprint.route('review', methods=['GET', 'POST'])
def review_movie():
    pass
