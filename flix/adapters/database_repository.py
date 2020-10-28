import csv
import os
from abc import ABC
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
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore exception and return None
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, movie_id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter_by(Movie.id == id).one()
        except NoResultFound:
            # Ignore exception and return None
            pass

        return movie

    def get_movies_by_letter(self, target_letter) -> List[Movie]:
        movies = self._session_cm.query(Movie).filter(Movie.first_letter == target_letter)
        return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.query(Movie).count()
        return number_of_movies

    def get_first_movie(self) -> Movie:
        movie = self._session_cm.query(Movie).first()
        return movie

    def get_first_letter(self, movie_id: int) -> str:
        movie = self.get_movie(movie_id)
        return movie.get_first_letter()

    def get_last_movie(self) -> Movie:
        movie = self._session_cm.query(Movie).order_by(desc(Movie.id)).first()

    def get_movies_from_year(self, year: int) -> List[Movie]:
        movies = self._session_cm.query(Movie).filter(Movie.year == year)
        return movies

    def get_letter_of_next_movie(self, movie: Movie):
        movie = self._session_cm.query(Movie).filter(Movie.first_letter > movie.first_letter).order_by(
            Movie.first_letter).first()
        return movie

    def get_letter_of_previous_movie(self, movie: Movie):
        movie = self._session_cm.query(Movie).filter(Movie.first_letter < movie.first_letter).order_by(
            desc(Movie.first_letter)).first()
        return movie

    def get_all_letters(self):
        # Optimise
        letters = list()
        movies = self._session_cm.query(Movie).all()
        for movie in movies:
            if movie.title[0] not in letters:
                letters.append(movie.title[0])
        letters.sort()
        return letters

    def alphabet(self):
        alphabet_list = ['Numbers']
        for i in range(0, 26):
            alphabet_list.append(chr(ord("A") + i))
        return alphabet_list

    def get_movies_from_genre(self, genre: Genre):
        movies = []
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
        genres = self._session_cm.query(Genre).all()
        return genres

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.query(Review).all()
        return reviews

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_actors(self) -> List[Actor]:
        actors = self._session_cm.query(Actor).all()
        return actors

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_directors(self) -> List[Director]:
        directors = self._session_cm.query(Director).all()
        return directors

    def get_actor(self, fullname: str):
        actor = self._session_cm.query(Actor).filter(Actor.actor_full_name == fullname).one()
        return actor

    def get_director(self, fullname: str):
        director = self._session_cm.query(Director).filter(Director.director_full_name == fullname).one()
        return director


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
                directors[movie_director] = list()
            directors[movie_director].append((director_index, movie_key))
            director_index += 1

            for actor in movie_actors:
                if actor not in actors.keys():
                    actors[actor] = list()
                actors[actor].append(movie_key)

            # Remove Genres, Actors, Director and unused data from data
            movie_data = movie_data[0:2] + [movie_data[3]] + [str(director_index)] + movie_data[6:8]
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
        director_records.append((director_key, director))


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
    id, title, description, director_id, year, runtime)
    VALUES (?, ?, ?, ?, ?, ?)"""
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
    VALUES (?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    conn.commit()
    conn.close()
