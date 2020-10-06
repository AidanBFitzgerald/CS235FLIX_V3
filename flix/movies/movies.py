from flask import Blueprint, request, url_for, render_template

# Configure Blueprint
from flix.adapters import repository as repo
from flix.movies import services

movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_letter', methods=['GET'])
def movies_by_letter():
    target_letter = request.args.get('letter')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if target_letter is None:
        movie_id = services.get_first_movie(repo.repo_instance)['id']
        target_letter = services.get_first_letter(movie_id, repo.repo_instance)

    movies, previous_letter, next_letter = services.get_movies_by_letter(target_letter, repo.repo_instance)
    alphabet = services.alphabet(repo.repo_instance)

    if movie_to_show_reviews is None:
        movie_to_show_reviews = -1
    else:
        movie_to_show_reviews = int(movie_to_show_reviews)

    return render_template('movies/movies_by_letter.html',
                           alphabet=alphabet,
                           movies=movies,
                           letter=target_letter
                           )


@movies_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    pass


@movies_blueprint.route('/review', methods=['GET', 'POST'])
def review_movie():
    pass


@movies_blueprint.route('/movie', methods=['GET'])
def movie():
    movie_id = int(request.args.get('movie_id'))
    movie_dict = services.get_movie(movie_id, repo.repo_instance)
    return render_template('movies/movie.html',
                           movie=movie_dict)
