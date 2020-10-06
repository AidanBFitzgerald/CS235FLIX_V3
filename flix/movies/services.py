from typing import Iterable

from flix.adapters.repository import AbstractRepository
from flix.domain.model import Movie, Review, Genre, make_review, Actor


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, rating, username: str, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create Review
    review = make_review(review_text, user, movie, rating)

    # Update Repo
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_all_letters(repo: AbstractRepository):
    return repo.get_all_letters()


def get_movies_by_letter(letter, repo: AbstractRepository):
    # Returns movies from a given letter (returns None if there are no matches), the previous letter and the next letter
    movies = repo.get_movies_by_letter(letter)
    movies_dict = list()
    prev_letter = None
    next_letter = None

    if len(movies) > 0:
        movies_dict = movies_to_dict(movies)
        prev_letter = repo.get_letter_of_previous_movie(movies[0])
        next_letter = repo.get_letter_of_next_movie(movies[0])

    return movies_dict, prev_letter, next_letter


def get_movies_from_genre(genre_name, repo: AbstractRepository):
    genre = Genre(genre_name)
    movies = repo.get_movies_from_genre(genre)
    return movies_to_dict(movies)


def get_reviews_for_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


# ============================================
# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'description': movie.description,
        'director': movie.director.director_full_name,
        'actors': [actor.actor_full_name for actor in movie.actors],
        'genres': genres_to_dict(movie.genres),
        'runtime': movie.runtime_minutes,
        'reviews': reviews_to_dict(movie.reviews),
        'id': movie.id,
        'title': movie.title,
        'year': movie.year
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.user_name,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre': genre.genre_name,
        'genre_movies': [movie.id for movie in genre.movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.year, dict.id)
    return movie
