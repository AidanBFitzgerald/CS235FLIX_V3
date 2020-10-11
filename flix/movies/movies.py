from better_profanity import profanity
from flask import Blueprint, request, url_for, render_template, session, redirect

# Configure Blueprint
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from flix.adapters import repository as repo
from flix.authentication.authentication import login_required
from flix.movies import services

movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_letter', methods=['GET'])
def movies_by_letter():
    target_letter = request.args.get('letter')
    cursor = request.args.get('cursor')
    movies_per_page = 10
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    watchlist = services.get_watchlist(repo.repo_instance)

    if target_letter is None:
        movie_id = services.get_first_movie(repo.repo_instance)['id']
        target_letter = services.get_first_letter(movie_id, repo.repo_instance)

    movies, previous_letter, next_letter = services.get_movies_by_letter(target_letter, repo.repo_instance)
    alphabet = services.alphabet(repo.repo_instance)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)
    if movies is not None:
        if cursor > 0:
            # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.movies_by_letter',
                                     letter=target_letter,
                                     cursor=cursor - movies_per_page)
            first_movie_url = url_for('movies_bp.movies_by_letter',
                                      letter=target_letter)

        if cursor + movies_per_page < len(movies):
            # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
            next_movie_url = url_for('movies_bp.movies_by_letter',
                                     letter=target_letter,
                                     cursor=cursor + movies_per_page)

            last_cursor = movies_per_page * int(len(movies) / movies_per_page)
            if len(movies) % movies_per_page == 0:
                last_cursor -= movies_per_page

            last_movie_url = url_for('movies_bp.movies_by_letter',
                                     letter=target_letter,
                                     cursor=last_cursor)

    # Get Movie for current page
    last_movie_index = cursor + movies_per_page
    movies = movies[cursor: last_movie_index]

    return render_template('movies/movies_by_letter.html',
                           alphabet=alphabet,
                           movies=movies,
                           letter=target_letter,
                           watchlist=watchlist,
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           next_movie_url=next_movie_url,
                           last_movie_url=last_movie_url
                           )


@movies_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    watchlist = services.get_watchlist(repo.repo_instance)
    search_result = []
    search = [request.args.get('search_genre'), request.args.get('search_actor'), request.args.get('search_director')]
    cursor = request.args.get('cursor')
    movies_per_page = 10
    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    if form.validate_on_submit():
        genre = form.genre.data
        actor = form.actor.data
        director = form.director.data
        return redirect(url_for('movies_bp.search', search_genre=genre, search_actor=actor, search_director=director))

    if search is not None:
        movies_genre = []
        movies_actor = []
        movies_director = []
        search_list = []

        genre = search[0]
        if genre != "" and genre is not None:
            genre = genre[0].upper() + genre[1:].lower()
            movies_genre = services.get_movies_from_genre(genre, repo.repo_instance)

        actor = search[1]
        if actor != "" and actor is not None:
            actor = services.get_actor(actor, repo.repo_instance)
            if actor is not None:
                movies_actor = actor['movies']

        director = search[2]
        if director != "" and director is not None:
            director = services.get_director(director, repo.repo_instance)
            if director is not None:
                movies_director = director['movies']
        search_list = [movies_genre, movies_actor, movies_director]

        # Remove search elements that are empty
        for i in range(len(search_list) - 1, -1, -1):
            if not search_list[i]:
                search_list.pop(i)

        # Find common movies for search parameters
        search_result = services.elements_in_common(search_list)

        if cursor > 0:
            # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movies_bp.search', search_genre=search[0],
                                     search_actor=search[1],
                                     search_director=search[2],
                                     cursor=cursor - movies_per_page)
            first_movie_url = url_for('movies_bp.search', search_genre=search[0],
                                      search_actor=search[1],
                                      search_director=search[2])

        if cursor + movies_per_page < len(search_result):
            # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
            next_movie_url = url_for('movies_bp.search', search_genre=search[0],
                                     search_actor=search[1],
                                     search_director=search[2],
                                     cursor=cursor + movies_per_page)
            last_cursor = movies_per_page * int(len(search_result) / movies_per_page)
            if len(search_result) % movies_per_page == 0:
                last_cursor -= movies_per_page

            last_movie_url = url_for('movies_bp.search', search_genre=search[0],
                                     search_actor=search[1],
                                     search_director=search[2],
                                     cursor=last_cursor)

        # Get Movie for current page
        last_movie_index = cursor + movies_per_page
        search_result = search_result[cursor: last_movie_index]

        # Get movies from movie ids
        for i in range(0, len(search_result)):
            search_result[i] = services.get_movie(search_result[i], repo.repo_instance)

    return render_template('movies/search.html',
                           search_result=search_result,
                           watchlist=watchlist,
                           form=form,
                           handler_url=url_for('movies_bp.search'),
                           prev_movie_url=prev_movie_url,
                           first_movie_url=first_movie_url,
                           next_movie_url=next_movie_url,
                           last_movie_url=last_movie_url
                           )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed article, from the form.
        movie_id = int(form.movie_id.data)
        rating = int(form.rating.data)
        services.add_review(movie_id, form.review.data, rating, username, repo.repo_instance)

        return redirect(url_for('movies_bp.movie', movie_id=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie_id'))

        # Store movie id in the form
        form.movie_id.data = movie_id

    else:
        # Request is a HTTP POST where form validation has failed.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST
    movie_dict = services.get_movie(movie_id, repo.repo_instance)
    watchlist = services.get_watchlist(repo.repo_instance)

    return render_template('movies/review_movie.html',
                           title='Review Movie',
                           form=form,
                           movie=movie_dict,
                           review_page=1,
                           handler_url=url_for('movies_bp.review_movie'),
                           watchlist=watchlist)


@movies_blueprint.route('/movie', methods=['GET'])
def movie():
    movie_id = int(request.args.get('movie_id'))
    movie_to_show_reviews = request.args.get('view_reviews_for')
    in_watchlist = request.args.get('in_watchlist')

    watchlist = services.get_watchlist(repo.repo_instance)
    movie_in_watchlist = services.movie_in_watchlist(watchlist, movie_id)

    if movie_to_show_reviews is None:
        movie_to_show_reviews = -1

    else:
        movie_to_show_reviews = int(movie_to_show_reviews)

    if in_watchlist is not None:
        if int(in_watchlist) == 1:
            services.add_to_watchlist(movie_id, repo.repo_instance)
            return redirect(url_for("movies_bp.movie", movie_id=movie_id, view_reviews_for=movie_to_show_reviews))
        if int(in_watchlist) == -1:
            services.remove_from_watchlist(movie_id, repo.repo_instance)
            return redirect(url_for("movies_bp.movie", movie_id=movie_id, view_reviews_for=movie_to_show_reviews))

    movie_dict = services.get_movie(movie_id, repo.repo_instance)
    movie_dict["view_review_url"] = url_for('movies_bp.movie', movie_id=movie_id, view_reviews_for=movie_id)
    movie_dict["add_review_url"] = url_for('movies_bp.review_movie', movie_id=movie_id)
    return render_template('movies/movie.html',
                           movie=movie_dict,
                           review_page=0,
                           show_reviews_for_movie=movie_to_show_reviews,
                           watchlist=watchlist,
                           movie_in_watchlist=movie_in_watchlist)


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = IntegerField('Rating', [
        DataRequired(),
        NumberRange(min=0, max=10, message="Rating is from 0-10")])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    genre = StringField("Genre")
    actor = StringField("Actor")
    director = StringField("Director")
    submit = SubmitField("Search")
