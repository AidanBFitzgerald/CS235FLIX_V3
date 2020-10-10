from better_profanity import profanity
from flask import Blueprint, request, url_for, render_template, session, redirect

# Configure Blueprint
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from flix.adapters import repository as repo
from flix.authentication.authentication import login_required
from flix.movies import services

movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/movies_by_letter', methods=['GET'])
def movies_by_letter():
    target_letter = request.args.get('letter')

    watchlist = services.get_watchlist(repo.repo_instance)

    if target_letter is None:
        movie_id = services.get_first_movie(repo.repo_instance)['id']
        target_letter = services.get_first_letter(movie_id, repo.repo_instance)

    movies, previous_letter, next_letter = services.get_movies_by_letter(target_letter, repo.repo_instance)
    alphabet = services.alphabet(repo.repo_instance)

    return render_template('movies/movies_by_letter.html',
                           alphabet=alphabet,
                           movies=movies,
                           letter=target_letter,
                           watchlist=watchlist
                           )


@movies_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    pass


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
