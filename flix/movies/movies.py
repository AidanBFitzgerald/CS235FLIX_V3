from flask import Blueprint, request, url_for, render_template

# Configure Blueprint
from flix.adapters import repository as repo
from flix.movies import services

movies_blueprint = Blueprint('movies.bp', __name__)


@movies_blueprint.route('/movies_by_letter', methods=['GET'])
def movies_by_letter():
    target_letter = request.args.get('letter')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if target_letter is None:
        target_letter = services.get_first_movie(repo.repo_instance)['title'][0]

    movies, previous_letter, next_letter = services.get_movies_by_letter(target_letter, repo.repo_instance)
    all_letters = services.get_all_letters()

    if movie_to_show_reviews is None:
        movie_to_show_reviews = -1
    else:
        movie_to_show_reviews = int(movie_to_show_reviews)

    first_in_letter_url = None
    last_in_letter_url = None
    next_in_letter_url = None
    previous_in_letter_url = None
    previous_letter_url = None
    next_letter_url = None

    if len(movies) > 0:
        first_in_letter = movies[0]
        last_in_letter = movies[-1]
        # first_in_letter_url = url_for()
        # last_in_letter_url = url_for()
        if previous_letter is not None:
            previous_letter_url = url_for('movies_bp.movies_by_letter', letter=previous_letter)
        if next_letter is not None:
            next_letter_url = url_for('movies_bp.movies_by_letter', letter=next_letter)

        render_template('movies/movies_by_letter',
                        first_in_letter_url=first_in_letter_url,
                        last_in_letter_url=last_in_letter_url,
                        next_in_letter_url=next_in_letter_url,
                        previous_in_letter_url=previous_in_letter_url,
                        previous_letter_url=previous_letter_url,
                        next_letter_url=next_letter_url
                        )


@movies_blueprint.route('search', methods=['GET', 'POST'])
def search():
    pass


@movies_blueprint.route('review', methods=['GET', 'POST'])
def review_movie():
    pass
