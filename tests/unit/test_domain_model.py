import pytest

from flix.domain.model import Director, User, Movie, Actor, Genre, make_review, WatchList


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def movie():
    return Movie("Guardians of the Galaxy", 2014, 1)


@pytest.fixture()
def actor():
    return Actor("Chris Pratt")


@pytest.fixture()
def genre():
    return Genre("Action")


@pytest.fixture()
def watchlist():
    return WatchList(User('shaun', '12345'))


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of reviews after construction.
        assert False


def test_director_construction():
    director1 = Director("Taika Waititi")
    assert repr(director1) == "<Director Taika Waititi>"
    director2 = Director("")
    assert director2.director_full_name is None
    director3 = Director(42)
    assert director3.director_full_name is None

    for movie in director1.movies:
        assert False


def test_genre_construction(genre):
    assert genre.genre_name == "Action"

    for movie in genre.movies:
        assert False


def test_watchlist_construction(watchlist):
    assert watchlist.watchlist == []


def test_movie_construction(movie):
    assert movie.id == 1
    assert movie.director is None
    assert movie.title == "Guardians of the Galaxy"
    assert movie.year == 2014
    assert movie.description is None
    assert movie.runtime_minutes is None
    for actor in movie.actors:
        assert False
    for genre in movie.genres:
        assert False
    for review in movie.reviews:
        assert False
    assert movie.get_first_letter() == "G"


def test_movie_less_than_operator(movie):
    movie2 = Movie("Prometheus", 2012, None)

    assert movie < movie2


def test_make_review_establishes_relationships(movie, user):
    review_text = "Action packed!"
    rating = 9
    review = make_review(review_text, user, movie, rating)

    # Check that user knows about review
    assert review in user.reviews

    # Check that review knows about user
    assert review.user is user

    # Check that movie knows about review
    assert review in movie.reviews

    # Check that review knows about movie
    assert review.movie is movie
