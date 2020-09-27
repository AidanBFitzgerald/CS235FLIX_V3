import pytest

from flix.domain.model import User, Movie, Genre, Review, Actor, Director


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
    movie = Movie("Kingsman", 2016)
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie("Kingsman", 2016) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie("Guardians of the Galaxy", 2014)

    # Check that the Movie has the expected title.
    assert movie.title == "Guardians of the Galaxy"


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie("dadasd", 1988)
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
    review = Review(Movie("asdsa", 2014), "Great Movie!", 9)
    in_memory_repo.add_review(review)
    reviews = in_memory_repo.get_reviews()
    assert len(reviews) == 1
    assert review in reviews


# ADD TEST FOR USER AND MOVIE LINK WITH REVIEW


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
