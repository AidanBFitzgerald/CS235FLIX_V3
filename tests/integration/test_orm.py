import datetime

import pytest

from flix.domain.model import Movie, User, Genre, Director


def insert_user(empty_session, values=None):
    new_name = "Aidan"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_director(empty_session):
    empty_session.execute('INSERT INTO directors (fullname) VALUES ("Henry Selick")')
    row = empty_session.execute('SELECT id from directors').fetchone()
    return row[0]


def insert_movie(empty_session):
    director_key = insert_director(empty_session)
    empty_session.execute(
        'INSERT INTO movies (title, year, description, runtime, director_id) VALUES'
        '("James and the Giant Peach", 1996, "An orphaned boy drops magical crocodile tongues which later grow into a '
        'never-ending peach tree. He finds his new family which are six insects that help him on his adventure.",'
        '84, :director_id) ', {"director_id": director_key}
    )
    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]


def insert_genre(empty_session):
    empty_session.execute('INSERT INTO genres (name) VALUES ("Adventure"), ("Family")')
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie_genre_associations(empty_session, movie_key, genre_keys):
    stmt = 'INSERT INTO movie_genres (movie_id, genre_id) VALUES (:movies_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {"movies_id": movie_key, 'genre_id': genre_key})


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute("INSERT INTO reviews (user_id, movie_id, review, rating, timestamp) VALUES"
                          "(:user_id, :movie_id, 'Review 1', 10, :timestamp_1),"
                          "(:user_id, :movie_id, 'Review 2', 3, :timestamp_2)",
                          {'user_id': user_key, 'movie_id': movie_key, 'timestamp_1': timestamp_1,
                           'timestamp_2': timestamp_2}
                          )

    row = empty_session.execute("SELECT id from movies")
    return row[0]


def make_director():
    director = Director("Henry Selick")
    return director


def make_movie():
    movie = Movie('James and the Giant Peach', 1996)
    return movie


def make_user():
    user = User("Aidan", "12222")
    return user


def make_genre():
    genre = Genre("Adventure")
    return genre


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

