from typing import List

from adapters.repository import AbstractRepository
from flix.domain.model import Director, Actor, Review, Genre, Movie, User


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.movies = list()
        self.users = list()
        self.genres = list()
        self.reviews = list()

    def add_user(self, user: User):
        pass

    def get_user(self, username) -> User:
        pass

    def add_movie(self, movie: Movie):
        pass

    def get_movie(self, title, year) -> Movie:
        pass

    def get_movies_by_letter(self, target_letter) -> List[Movie]:
        pass

    def get_number_of_movies(self):
        pass

    def get_first_movie(self) -> Movie:
        pass

    def get_last_movie(self) -> Movie:
        pass

    def get_movies_by_year(self, year: int) -> List[Movie]:
        pass

    def get_movies_from_genre(self, genre: Genre):
        pass

    def add_genre(self):
        pass

    def get_genres(self) -> List[Genre]:
        pass

    def add_review(self, review: Review):
        pass

    def get_reviews(self):
        pass

    def add_actor(self, actor: Actor):
        pass

    def get_actors(self) -> List[Actor]:
        pass

    def add_director(self, director: Director):
        pass

    def get_directors(self) -> List[Director]:
        pass
