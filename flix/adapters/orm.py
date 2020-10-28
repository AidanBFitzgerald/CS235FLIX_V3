from sqlalchemy import (
    Table, Column, Integer, String, DateTime,
    ForeignKey, MetaData
)
from sqlalchemy.orm import mapper, relationship

from flix.domain import model

metadata = MetaData()

users = Table('users', metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('username', String(255), unique=True, nullable=False),
              Column('password', String(255), nullable=False)
              )

reviews = Table('reviews', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('user_id', Integer, ForeignKey('users.id')),
                Column('movie_id', Integer, ForeignKey('movies.id')),
                Column('review', String(1024), nullable=False),
                Column('rating', Integer, nullable=False),
                Column('timestamp', DateTime, nullable=False)
                )

movies = Table('movies', metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('title', String(255), nullable=False),
               Column('year', Integer, nullable=False),
               Column('description', String(1024), nullable=False),
               Column('director_id', Integer, ForeignKey("directors.id")),
               Column('runtime', Integer, nullable=False)
               )

genres = Table('genres', metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('name', String(255), nullable=False)
               )

movie_genres = Table('movie_genres', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('movie_id', Integer, ForeignKey('movies.id')),
                     Column('genre_id', ForeignKey('genres.id'))
                     )

directors = Table('directors', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('fullname', String(255), nullable=False)
                  )

actors = Table('actors', metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('fullname', String(255), nullable=False)
               )

movie_actors = Table('movie_actors', metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('movie_id', Integer, ForeignKey('movies.id')),
                     Column('actor_id', Integer, ForeignKey('actors.id'))
                     )


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review_text': reviews.c.review,
        '_rating': reviews.c.rating,
        '_timestamp': reviews.c.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_title': movies.c.title,
        '_year': movies.c.year,
        '_description': movies.c.description,
        '_runtime_minutes': movies.c.runtime,
        '_reviews': relationship(model.Review, backref='_movie')
    })
    mapper(model.Genre, genres, properties={
        '_genre_name': genres.c.name,
        '_movies': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref='_genres'
        )
    })
    mapper(model.Director, directors, properties={
        '_director_full_name': directors.c.fullname,
        '_movies': relationship(model.Movie, backref='_director')
    })
    mapper(model.Actor, actors, properties={
        '_actor_full_name': actors.c.fullname,
        '_movies': relationship(
            movies_mapper,
            secondary=movie_actors,
            backref='_actors')
    })
