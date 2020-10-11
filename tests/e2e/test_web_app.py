import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('shaun', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'shaun'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235FLIX is a movie' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review?movie_id=2')

    response = client.post(
        '/review',
        data={'review': 'Bad movie', 'movie_id': 2, 'rating': 3}
    )
    assert response.headers['Location'] == 'http://localhost/movie?movie_id=2'


@pytest.mark.parametrize(('review', 'messages', 'rating'), (
        ('fuck this movie', (b'Your review must not contain profanity'), 8),
        ('Hey', b'Your review is too short', 8),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity'), 8),
        ("Great movie", b"Rating is from 0-10", -1)
))
def test_review_with_invalid_input(client, auth, review, messages, rating):
    # Login a user.
    auth.login()

    # Attempt to review on movie.
    response = client.post(
        '/review',
        data={'review': review, 'movie_id': 2, 'rating': rating}
    )
    # Check that supplying invalid comment text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movies_without_letter(client):
    # Check that we can retrieve the movies letter page
    response = client.get('/movies_by_letter')
    assert response.status_code == 200

    # Check correct movies page displayed
    assert b'Guardians of the Galaxy' in response.data


def test_movies_with_letter(client):
    # Check that we can retrieve the movies letter page
    response = client.get('/movies_by_letter?letter=S')
    assert response.status_code == 200

    # Check correct movies page displayed
    assert b'Split' in response.data
    assert b'Sing' in response.data


def test_movies_with_review(client, auth):
    auth.login()
    response = client.get('/review?movie_id=2')
    # Create review
    client.post(
        '/review',
        data={'review': 'Bad movie', 'movie_id': 2, 'rating': 3}
    )

    response = client.get('/movie?movie_id=2&view_reviews_for=2')
    assert response.status_code == 200

    # Check comment is included in page
    assert b'Bad movie' in response.data


def test_movies_with_search(client):
    response = client.get('/search?search_genre=Action&search_actor=Chris Pratt&search_director=James Gunn')
    assert response.status_code == 200

    assert b'Guardians of the Galaxy' in response.data
    assert b'Prometheus' not in response.data
