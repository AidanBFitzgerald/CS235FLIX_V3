from datetime import datetime

import pytest

from flix.adapters.repository import RepositoryException
from flix.domain.model import User, Movie, Genre, Review, Actor, Director, make_review


def test_repository_can_add_a_user(in_memory_repo):
    user = User("aidan", "1234567890")
    in_memory_repo.add_user(user)
    assert in_memory_repo.get_user("aidan") is user


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('sam')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 5 movies
    assert number_of_movies == 5


def test_repository_can_add_a_movie(in_memory_repo):
    movie = Movie("Kingsman", 2016, 6)
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(6) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"
    assert movie.id == 1


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(7)
    assert movie is None


def test_repository_can_retrieve_movies_by_letter(in_memory_repo):
    movies = in_memory_repo.get_movies_by_letter('S')

    # Check that query returned 3 articles
    assert len(movies) == 3


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_letter(in_memory_repo):
    movies = in_memory_repo.get_movies_by_letter('A')

    assert len(movies) == 0


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == "Guardians of the Galaxy"


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == "Suicide Squad"


def test_repository_can_get_movies_from_year(in_memory_repo):
    movies = in_memory_repo.get_movies_from_year(2012)
    assert len(movies) == 1
    assert movies[0].title == "Prometheus"


def test_repository_can_get_next_movie_letter(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    next_movie_letter = in_memory_repo.get_letter_of_next_movie(movie)
    assert next_movie_letter == 'P'


def test_repository_can_get_previous_movie_letter(in_memory_repo):
    movie = in_memory_repo.get_movie(5)
    prev_movie_letter = in_memory_repo.get_letter_of_previous_movie(movie)
    assert prev_movie_letter == "P"


def test_repository_retrieves_all_letters(in_memory_repo):
    letters = in_memory_repo.get_all_letters()
    assert len(letters) == 3
    assert letters[0] == 'G'


def test_repository_returns_an_empty_list_when_there_are_none_for_given_date(in_memory_repo):
    movies = in_memory_repo.get_movies_from_year(2077)
    assert len(movies) == 0


def test_repository_can_add_genre(in_memory_repo):
    genre = Genre("Indie")
    in_memory_repo.add_genre(genre)
    assert genre in in_memory_repo.get_genres()


def test_repository_can_retrieve_genres(in_memory_repo):
    genres = in_memory_repo.get_genres()
    assert len(genres) == 10
    assert Genre("Action") in genres


def test_repository_can_get_movies_from_genre(in_memory_repo):
    movies = in_memory_repo.get_movies_from_genre(Genre("Action"))
    assert len(movies) == 2
    assert movies[0].title == "Guardians of the Galaxy"
    assert movies[1].title == "Suicide Squad"


def test_repository_returns_an_empty_list_where_there_are_no_movies_in_a_genre(in_memory_repo):
    movies = in_memory_repo.get_movies_from_genre("Indie")
    assert len(movies) == 0


def test_repository_can_add_a_review(in_memory_repo):
    user = User('aidan', 'hi1234')
    movie = Movie("asdsa", 2014)
    review = make_review("Wow good movie", user, movie, 9)
    in_memory_repo.add_review(review)
    reviews = in_memory_repo.get_reviews()
    assert len(reviews) == 1
    assert review in reviews


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = Movie("asdsa", 2014)
    review = Review(None, movie, "Wow", 8, datetime.today())
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = User('aidan', 'hi1234')
    movie = Movie("asdsa", 2014)
    review = Review(user, movie, "Wow good movie", 9, datetime.today())
    user.add_review(review)
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_returns_an_empty_list_where_there_no_reviews(in_memory_repo):
    reviews = in_memory_repo.get_reviews()
    assert len(reviews) == 0


def test_repository_can_add_a_actor(in_memory_repo):
    actor = Actor("Dave Brown")
    in_memory_repo.add_actor(actor)
    assert actor in in_memory_repo.get_actors()


def test_repository_can_retrieve_actors(in_memory_repo):
    actors = in_memory_repo.get_actors()
    assert len(actors) == 20
    assert Actor("Chris Pratt") in actors


def test_repository_can_add_a_director(in_memory_repo):
    director = Director("Fred")
    in_memory_repo.add_director(director)
    assert director in in_memory_repo.get_directors()


def test_repository_can_retrieve_directors(in_memory_repo):
    directors = in_memory_repo.get_directors()
    assert len(directors) == 5
    assert Director("James Gunn") in directors
