import pytest

from flix.authentication.services import AuthenticationException
from flix.domain.model import make_review, User
from flix.movies import services as movies_services
from flix.authentication import services as auth_services


def test_can_add_review(in_memory_repo):
    movie_id = 1
    review_text = "Wasn't a fan"
    rating = 4
    username = 'shaun'

    movies_services.add_review(movie_id, review_text, rating, username, in_memory_repo)
    comments_as_dict = movies_services.get_reviews_for_movie(movie_id, in_memory_repo)

    assert next(
        (dictionary['review_text'] for dictionary in comments_as_dict if dictionary["review_text"] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 12
    review_text = 'Favourite Movie!'
    rating = 10
    user = 'shaun'

    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_id, review_text, rating, user, in_memory_repo)


def test_cannot_add_review_for_non_existent_user(in_memory_repo):
    movie_id = 2
    review_text = 'Favourite Movie!'
    rating = 10
    user = 'dave'

    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_id, review_text, rating, user, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2
    movie_as_dict = movies_services.get_movie(movie_id, in_memory_repo)
    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict[
               'description'] == "Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone."
    assert movie_as_dict['title'] == "Prometheus"
    assert movie_as_dict['director'] == "Ridley Scott"
    assert movie_as_dict['actors'] == ["Noomi Rapace", "Logan Marshall-Green", "Michael Fassbender", "Charlize Theron"]
    assert movie_as_dict['genres'][0]["genre"] == "Adventure"
    assert movie_as_dict['runtime'] == 124
    assert len(movie_as_dict['reviews']) == 0
    assert movie_as_dict['year'] == 2012


def test_cannot_get_non_existent_movie(in_memory_repo):
    movie_id = 27
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_can_get_first_movie(in_memory_repo):
    movie = movies_services.get_first_movie(in_memory_repo)
    assert movie['id'] == 1


def test_can_get_last_movie(in_memory_repo):
    movie = movies_services.get_last_movie(in_memory_repo)
    assert movie['id'] == 5


def test_can_get_all_letters(in_memory_repo):
    letters = movies_services.get_all_letters(in_memory_repo)
    assert len(letters) == 3
    assert letters[0] == 'G'


def test_can_get_movies_by_letter(in_memory_repo):
    letter = 'P'
    movies, prev_letter, next_letter = movies_services.get_movies_by_letter(letter, in_memory_repo)
    assert movies[0]['id'] == 2
    assert prev_letter == 'G'
    assert next_letter == 'S'


def test_can_get_movies_from_genre(in_memory_repo):
    genre = "Action"
    movies = movies_services.get_movies_from_genre(genre, in_memory_repo)
    assert movies[0] == 1
    assert movies[1] == 5


def test_can_get_reviews_for_movie(in_memory_repo):
    movie_id = 1

    # adding review to repo
    user = User("shaun", '12345')
    review = make_review("Wow", user, in_memory_repo.get_movie(1), 10)
    in_memory_repo.add_review(review)

    # testing retrieval of review
    reviews = movies_services.get_reviews_for_movie(movie_id, in_memory_repo)
    assert len(reviews) == 1
    assert reviews[0]["review_text"] == "Wow"


def test_cannot_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(movies_services.NonExistentMovieException):
        reviews = movies_services.get_reviews_for_movie(12, in_memory_repo)


def test_can_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews) == 0


def test_can_get_actor(in_memory_repo):
    actor = movies_services.get_actor("Chris Pratt", in_memory_repo)
    assert actor['fullname'] == "Chris Pratt"
    assert len(actor['movies']) > 0


def test_can_get_director(in_memory_repo):
    director = movies_services.get_director("James Gunn", in_memory_repo)
    assert director['fullname'] == "James Gunn"
    assert len(director['movies']) > 0


def test_common_elements(in_memory_repo):
    actor_movies = movies_services.get_actor("Chris Pratt", in_memory_repo)['movies']
    director_movies = movies_services.get_director("James Gunn", in_memory_repo)['movies']
    genre_movies = movies_services.get_movies_from_genre("Action", in_memory_repo)
    assert len(actor_movies) > 0
    assert len(director_movies) > 0
    assert len(genre_movies) > 0
    common = movies_services.elements_in_common([genre_movies, actor_movies, director_movies])
    assert len(common) == 1
    assert 1 in common


def test_nothing_in_common(in_memory_repo):
    actor_movies = movies_services.get_actor("Chris Pratt", in_memory_repo)['movies']
    director_movies = movies_services.get_director("Ridley Scott", in_memory_repo)['movies']
    genre_movies = movies_services.get_movies_from_genre("Action", in_memory_repo)
    assert len(actor_movies) > 0
    assert len(director_movies) > 0
    assert len(genre_movies) > 0
    common = movies_services.elements_in_common([genre_movies, actor_movies, director_movies])
    assert len(common) == 0


def test_can_add_user(in_memory_repo):
    username = "james"
    password = 'abcd1A23'

    auth_services.add_user(username, password, in_memory_repo)

    user = auth_services.get_user(username, in_memory_repo)
    assert user['username'] == username

    # Check password is encrypted
    assert user['password'].startswith("pbkdf2:sha256:")


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'shaun'
    password = "12345"

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    username = 'aidan'
    password = '12345'

    auth_services.add_user(username, password, in_memory_repo)

    try:
        auth_services.authenticate_user(username, password, in_memory_repo)

    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    username = 'aidan'
    password = '12345'

    auth_services.add_user(username, password, in_memory_repo)

    with pytest.raises(AuthenticationException):
        auth_services.authenticate_user(username, "abcdefg", in_memory_repo)
