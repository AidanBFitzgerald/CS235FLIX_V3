import csv
import os
from typing import List

from sqlalchemy import desc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack
from sqlalchemy.orm.exc import NoResultFound

from flix.adapters.repository import AbstractRepository
from flix.domain.model import Director, Actor, Review, Genre, Movie, User

genres = None
directors = None
actors = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        username = username.lower()
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, movie_id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == movie_id).one()
        except NoResultFound:
            # Ignore exception and return None
            pass

        return movie

    def get_movies_by_letter(self, target_letter) -> List[Movie]:
        # Optimise
        movies = self._session_cm.session.query(Movie).all()
        ret_list = []
        for movie in movies:
            if self.get_first_letter(movie.id) == target_letter:
                ret_list.append(movie)
            if target_letter == "Numbers":
                if self.get_first_letter(movie.id).isdigit():
                    ret_list.append(movie)
        return ret_list

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self) -> Movie:
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_first_letter(self, movie_id: int) -> str:
        movie = self.get_movie(movie_id)
        return movie.get_first_letter()

    def get_last_movie(self) -> Movie:
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie._id)).first()
        return movie

    def get_movies_from_year(self, year: int) -> List[Movie]:
        movies = self._session_cm.session.query(Movie).filter(Movie._year == year).all()
        return movies

    def get_letter_of_next_movie(self, movie: Movie):
        letter = None
        movie = self._session_cm.session.query(Movie).filter(Movie._first_letter > movie.first_letter).order_by(
            Movie._first_letter).first()
        if letter is not None:
            letter = movie.get_first_letter()
        return letter

    def get_letter_of_previous_movie(self, movie: Movie):
        letter = None
        movie = self._session_cm.session.query(Movie).filter(Movie._first_letter < movie.first_letter).order_by(
            desc(Movie._first_letter)).first()
        if letter is not None:
            letter = movie.get_first_letter()
        return letter

    def get_all_letters(self):
        # Optimise
        letters = list()
        movies = self._session_cm.session.query(Movie).all()
        for movie in movies:
            if movie.get_first_letter() not in letters:
                letters.append(movie.get_first_letter())
        letters.sort()
        return letters

    def alphabet(self):
        alphabet_list = ['Numbers']
        for i in range(0, 26):
            alphabet_list.append(chr(ord("A") + i))
        return alphabet_list

    def get_movies_from_genre(self, genre: Genre):
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name',
                                               {"genre_name": genre.genre_name}).fetchone()
        if row is None:
            movies = list()
        else:
            genre_id = row[0]

            movies = self._session_cm.session.execute('SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id '
                                                      'ORDER BY movie_id ASC',
                                                      {'genre_id': genre_id})
            movies = [id[0] for id in movies]

        return movies

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_actors(self) -> List[Actor]:
        actors = self._session_cm.session.query(Actor).all()
        return actors

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_directors(self) -> List[Director]:
        directors = self._session_cm.session.query(Director).all()
        return directors

    def get_actor(self, fullname: str):
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).filter(Actor._actor_full_name == fullname).one()
        except NoResultFound:
            # Ignore exception and return None
            pass
        return actor

    def get_director(self, fullname: str):
        director = None
        try:
            director = self._session_cm.session.query(Director).filter(Director._director_full_name == fullname).one()
        except NoResultFound:
            # Ignore exception and return None
            pass
        return director

    def add_to_watchlist(self, username: str, movie_id: int):
        user = self._session_cm.session.query(User).filter(User._username == username).one()
        movie = self._session_cm.session.query(Movie).filter(Movie._id == movie_id).one()
        user.add_to_watchlist(movie)
        self._session_cm.commit()

    def remove_from_watchlist(self, username: str, movie_id: int):
        user = self._session_cm.session.query(User).filter(User._username == username).one()
        movie = self._session_cm.session.query(Movie).filter(Movie._id == movie_id).one()
        user.remove_from_watchlist(movie)
        print(user._watchlist)
        self._session_cm.commit()


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        director_index = 0
        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            movie_data = row
            movie_key = movie_data[0]

            movie_genres = movie_data[2].split(',')
            movie_director = movie_data[4]
            movie_actors = movie_data[5].split(',')

            for genre in movie_genres:
                if genre not in genres.keys():
                    genres[genre] = list()
                genres[genre].append(movie_key)

            if movie_director not in directors.keys():
                director_index += 1
                directors[movie_director] = list()
                directors[movie_director].append(director_index)
            directors[movie_director].append(movie_key)

            for actor in movie_actors:
                if actor not in actors.keys():
                    actors[actor] = list()
                actors[actor].append(movie_key)

            # Remove Genres, Actors, Director and unused data from data
            movie_title = movie_data[1]

            letter_found = False

            for letter in movie_title:
                if 65 <= ord(letter) <= 90:
                    first_letter = letter
                    letter_found = True
                    break
            for letter in movie_title:
                if letter_found:
                    break
                if 48 <= ord(letter) <= 57:
                    first_letter = letter
                    break

            movie_data = movie_data[0:2] + [movie_data[3]] + [director_index] + movie_data[6:8] + [first_letter]
            yield movie_data


def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        genre_records.append((genre_key, genre))

    return genre_records


def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        for movie_key in genres[genre]:
            movie_genres_key += 1
            yield movie_genres_key, movie_key, genre_key


def get_director_records():
    director_records = list()

    for director in directors.keys():
        director_key = directors[director][0]
        director_records.append([director_key, director])

    return director_records


def get_actor_records():
    actor_records = list()
    actor_key = 0

    for actor in actors.keys():
        actor_key += 1
        actor_records.append((actor_key, actor))

    return actor_records


def movie_actors_generator():
    movie_actors_key = 0
    actors_key = 0

    for actor in actors.keys():
        actors_key += 1
        for movie_key in actors[actor]:
            movie_actors_key += 1
            yield movie_actors_key, movie_key, actors_key


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    global directors
    global actors
    genres = dict()
    directors = dict()
    actors = dict()

    insert_movies = """
    INSERT INTO movies (
    id, title, description, director_id, year, runtime, first_letter)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'movies.csv')))

    insert_genres = """
    INSERT INTO genres (id, name)
    VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_movie_genres = """
    INSERT INTO movie_genres (id, movie_id, genre_id)
    VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_directors = """
    INSERT INTO directors (id, fullname)
    VALUES (?, ?)"""
    cursor.executemany(insert_directors, get_director_records())

    insert_actors = """
    INSERT INTO actors (id, fullname)
    VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())

    insert_movie_actors = """
    INSERT INTO movie_actors (id, movie_id, actor_id)
    VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    conn.commit()
    conn.close()
