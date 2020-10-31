from datetime import datetime

import pytest

from flix.adapters.database_repository import SqlAlchemyRepository
from flix.adapters.repository import RepositoryException
from flix.domain.model import User, Movie, Director, Genre, make_review, Review, Actor


@pytest.fixture
def database(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_user(User('freddy', '123231'))
    return repo


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Liam', '123456789')
    repo.add_user(user)

    repo.add_user(User('Trevor', '123456789'))

    user2 = repo.get_user('Liam')

    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(database):
    repo = database

    user = repo.get_user('freddy')
    assert user == User('freddy', '123456789')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    count = repo.get_number_of_movies()

    assert count == 1000


def test_repository_can_add_a_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie1 = Movie("Sam I am", 2000)
    movie1.description = "Sam is sam he is"
    movie1.director = Director('James')
    movie1.runtime_minutes = 140
    repo.add_movie(movie1)
    movie = repo.get_movie(1001)

    assert movie == Movie('Sam I am', 2000)


def test_repository_can_retrieve_a_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie(1)

    assert movie.title == "Guardians of the Galaxy"
    assert movie.year == 2014
    assert movie.runtime_minutes == 121
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."


def test_repository_does_not_retrieve_non_existent_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie(1002)

    assert movie is None


def test_repository_can_retrieve_movies_by_letter(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_by_letter('G')

    assert movies[0].title == "Guardians of the Galaxy"
    assert len(movies) == 24


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_letter(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_by_letter('23')

    assert len(movies) == 0


def test_repository_can_get_first_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_first_movie()

    assert movie == Movie('Guardians of the Galaxy', 2014)


def test_repository_can_get_last_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_last_movie()

    assert movie == Movie('Nine Lives', 2016)


def test_repository_can_get_next_movie_letter(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    letter = repo.get_letter_of_next_movie(Movie('Guardians of the Galaxy', 2014))

    assert letter == 'H'


def test_repository_can_get_previous_movie_letter(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    letter = repo.get_letter_of_previous_movie(Movie('Guardians of the Galaxy', 2014))

    assert letter == 'F'


def test_repository_retrieves_all_letters(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    letters = repo.get_all_letters()

    assert len(letters) == 31
    assert letters[0] == '1'


def test_repository_returns_an_empty_list_when_there_are_none_for_given_date(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_from_year(2077)

    assert len(movies) == 0


def test_repository_can_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre('Indie')
    repo.add_genre(genre)
    assert genre in repo.get_genres()


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genres()
    assert len(genres) == 20
    assert Genre("Action") in genres


def test_repository_can_get_movies_from_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_from_genre(Genre('Comedy'))
    assert len(movies) == 279
    assert movies[0] == 4
    assert movies[1] == 7


def test_repository_returns_an_empty_list_where_there_are_no_movies_in_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_from_genre(Genre('Giraffe'))

    assert len(movies) == 0


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('aidan', 'hi1234')
    movie = Movie("Asdsa", 2014)
    movie.description = "Sam is sam he is"
    movie.director = Director('James')
    movie.runtime_minutes = 140
    review = make_review("Wow good movie", user, movie, 9)

    repo.add_user(user)
    repo.add_movie(movie)
    repo.add_review(review)

    reviews = repo.get_reviews()
    assert len(reviews) == 1
    assert review in reviews


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = Movie("Asdsa", 2014)
    movie.description = "Sam is sam he is"
    movie.director = Director('James')
    movie.runtime_minutes = 140
    repo.add_movie(movie)
    review = Review(None, movie, "Wow", 8, datetime.today())
    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User('aidan', 'hi1234')

    review = Review(user, None, "Wow good movie", 9, datetime.today())
    user.add_review(review)
    repo.add_user(user)
    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repository_returns_an_empty_list_where_there_no_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    reviews = repo.get_reviews()
    assert len(reviews) == 0


def test_repository_can_add_a_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    actor = Actor("Dave Brown")
    repo.add_actor(actor)
    assert actor in repo.get_actors()


def test_repository_can_retrieve_actors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    actors = repo.get_actors()

    assert len(actors) == 2394
    assert Actor("Chris Pratt") in actors


def test_repository_can_add_a_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    director = Director("Fred")

    repo.add_director(director)

    assert director in repo.get_directors()


def test_repository_can_retrieve_directors(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    directors = repo.get_directors()
    assert len(directors) == 644
    assert Director("James Gunn") in directors


def test_repository_can_retrieve_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    name = "Chris Pratt"
    actor = repo.get_actor(name)
    assert actor.actor_full_name == "Chris Pratt"


def test_repository_returns_none_for_non_existent_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    name = "Dave Sam"
    actor = repo.get_actor(name)
    assert actor is None


def test_repository_can_retrieve_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    name = "James Gunn"
    director = repo.get_director(name)

    assert director.director_full_name == name


def test_repository_returns_none_for_non_existent_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    name = "Sam sam"
    director = repo.get_director(name)
    assert director is None
