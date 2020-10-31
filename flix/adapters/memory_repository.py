import csv
import os
from bisect import insort_left
from typing import List

from flix.adapters.repository import AbstractRepository
from flix.domain.model import Director, Actor, Review, Genre, Movie, User


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__dataset_of_movies = list()
        self.__dataset_of_users = list()
        self.__dataset_of_actors = list()
        self.__dataset_of_directors = list()
        self.__dataset_of_genres = list()
        self.__dataset_of_reviews = list()
        self.__movies_index = dict()

    def add_user(self, user: User):
        if user not in self.__dataset_of_users:
            self.__dataset_of_users.append(user)

    def get_user(self, username) -> User:
        for user in self.__dataset_of_users:
            if user.username == username:
                return user

    def add_movie(self, movie: Movie):
        if movie not in self.__dataset_of_movies:
            insort_left(self.__dataset_of_movies, movie)
            self.__movies_index[movie.id] = movie

    def get_movie(self, movie_id: int) -> Movie:
        movie = None
        try:
            movie = self.__movies_index[movie_id]
        except KeyError:
            pass

        return movie

    def get_movies_by_letter(self, target_letter) -> List[Movie]:
        ret_list = []
        for movie in self.__dataset_of_movies:
            if self.get_first_letter(movie.id) == target_letter:
                ret_list.append(movie)
            if target_letter == "Numbers":
                if self.get_first_letter(movie.id).isdigit():
                    ret_list.append(movie)
        return ret_list

    def get_number_of_movies(self):
        return len(self.__dataset_of_movies)

    def get_first_movie(self) -> Movie:
        if len(self.__dataset_of_movies) > 0:
            return self.__dataset_of_movies[0]

    def get_first_letter(self, movie_id: int):
        movie = self.get_movie(movie_id)
        return movie.get_first_letter()

    def get_last_movie(self) -> Movie:
        if len(self.__dataset_of_movies) > 0:
            return self.__dataset_of_movies[-1]

    def get_movies_from_year(self, year: int) -> List[Movie]:
        year_match = []
        for movie in self.__dataset_of_movies:
            if movie.year == year:
                year_match.append(movie)
        return year_match

    def get_letter_of_next_movie(self, movie: Movie):
        next_letter = None
        try:
            index = self.__dataset_of_movies.index(movie)
            for sorted_movie in self.__dataset_of_movies[index + 1:]:
                if self.get_first_letter(sorted_movie.id) > self.get_first_letter(movie.id):
                    next_letter = self.get_first_letter(sorted_movie.id)
                    break
        except ValueError:
            pass
        except TypeError:
            pass
        return next_letter

    def get_letter_of_previous_movie(self, movie: Movie):
        previous_letter = None
        try:
            index = self.__dataset_of_movies.index(movie)
            for sorted_movie in reversed(self.__dataset_of_movies[:index]):
                if self.get_first_letter(sorted_movie.id) < self.get_first_letter(movie.id):
                    previous_letter = self.get_first_letter(sorted_movie.id)
                    break
        except ValueError:
            pass
        except TypeError:
            pass
        return previous_letter

    def get_all_letters(self):
        letters = list()
        for movie in self.__dataset_of_movies:
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
        genre_match = []
        for movie in self.__dataset_of_movies:
            if genre in movie.genres:
                genre_match.append(movie.id)
        return genre_match

    def add_genre(self, genre: Genre):
        if genre not in self.__dataset_of_genres:
            self.__dataset_of_genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__dataset_of_genres

    def add_review(self, review: Review):
        super().add_review(review)
        if review not in self.__dataset_of_reviews:
            self.__dataset_of_reviews.append(review)

    def get_reviews(self) -> List[Review]:
        return self.__dataset_of_reviews

    def add_actor(self, actor: Actor):
        if actor not in self.__dataset_of_actors:
            self.__dataset_of_actors.append(actor)

    def get_actors(self) -> List[Actor]:
        return self.__dataset_of_actors

    def add_director(self, director: Director):
        if director not in self.__dataset_of_directors:
            self.__dataset_of_directors.append(director)

    def get_directors(self) -> List[Director]:
        return self.__dataset_of_directors

    def get_actor(self, fullname: str):
        for actor in self.__dataset_of_actors:
            if actor.actor_full_name == fullname:
                return actor

    def get_director(self, fullname: str):
        for director in self.__dataset_of_directors:
            if director.director_full_name == fullname:
                return director

    def add_to_watchlist(self, username: str, movie_id: int):
        for user in self.__dataset_of_users:
            if user.username == username:
                for movie in self.__dataset_of_movies:
                    if movie.id == movie_id:
                        user.add_to_watchlist(movie)

    def remove_from_watchlist(self, username: str, movie_id: int):
        for user in self.__dataset_of_users:
            if user.username == username:
                for movie in self.__dataset_of_movies:
                    if movie.id == movie_id:
                        user.remove_from_watchlist(movie)

    def read_csv_file(self, file_name):
        with open(file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            for row in movie_file_reader:
                id = int(row['Rank'])
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year, id)
                self.add_movie(movie)
                actors = row["Actors"]
                actors = actors.split(",")
                for actor in actors:
                    actor = Actor(actor)
                    self.add_actor(actor)
                    actor = self.get_actor(actor.actor_full_name)
                    movie.add_actor(actor)
                    actor.add_movie(movie)

                director = Director(row["Director"])
                self.add_director(director)
                director = self.get_director(director.director_full_name)
                movie.director = director
                director.add_movie(movie)

                genres = row["Genre"]
                genres = genres.split(",")
                for genre in genres:
                    genre = Genre(genre)
                    movie.add_genre(genre)
                    self.add_genre(genre)

                movie.description = row["Description"]
                movie.runtime_minutes = int(row["Runtime (Minutes)"])


def populate(data_path: str, repo: MemoryRepository):
    repo.read_csv_file(os.path.join(data_path, 'movies.csv'))
