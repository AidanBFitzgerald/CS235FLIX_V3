from datetime import datetime


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.actor_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return self.actor_full_name == other.actor_full_name

    def __lt__(self, other):
        if not isinstance(other, Actor):
            return False
        return self.actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague):
        if colleague not in self.__colleagues and isinstance(colleague, Actor):
            self.__colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self.__colleagues:
            return True
        return False


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return self.director_full_name == other.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.director_full_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.genre_name == other.genre_name

    def __lt__(self, other):
        if not isinstance(other, Genre):
            return False
        return self.genre_name < other.genre_name

    def __hash__(self):
        return hash(self.genre_name)


class Movie:
    def __init__(self, title: str, year: int):
        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__reviews = []

        if year >= 1900:
            self.__year = year
        else:
            self.__year = None
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

    @property
    def title(self) -> str:
        return self.__title

    @property
    def year(self) -> int:
        return self.__year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> list:
        return self.__actors

    @property
    def genres(self) -> list:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def reviews(self):
        return self.__reviews

    @title.setter
    def title(self, new_title: str):
        if new_title == "" or type(new_title) is not str:
            self.__title = None
        else:
            self.__title = new_title.strip()

    @description.setter
    def description(self, new_description: str):
        if new_description == "" or type(new_description) is not str:
            self.__description = None
        else:
            self.__description = new_description.strip()

    @director.setter
    def director(self, new_director: Director):
        if isinstance(new_director, Director):
            self.__director = new_director

    @actors.setter
    def actors(self, new_actors: list):
        if type(new_actors) is list:
            self.__actors = new_actors

    @genres.setter
    def genres(self, new_genres):
        if type(new_genres) is list:
            self.__genres = new_genres

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime: int):
        if type(new_runtime) is int:
            if new_runtime <= 0:
                raise ValueError
            self.__runtime_minutes = new_runtime

    @reviews.setter
    def reviews(self, new_reviews):
        if type(new_reviews) is list:
            self.__reviews = new_reviews

    def add_review(self, review: 'Review'):
        if type(review) is Review:
            self.__reviews.append(review)

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.__title == other.__title and self.__year == other.__year

    def __lt__(self, other):
        if isinstance(other, Movie):
            if self.__title == other.title:
                return self.__year < other.__year
            else:
                return self.__title < other.title
        return False

    def __hash__(self):
        return hash((self.__title, self.__year))

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor) and actor not in self.__actors:
            self.__actors.append(actor)

    def remove_actor(self, actor):
        try:
            self.__actors.remove(actor)

        except ValueError:
            return

    def add_genre(self, genre):
        if isinstance(genre, Genre) and genre not in self.__genres:
            self.__genres.append(genre)

    def remove_genre(self, genre):
        try:
            self.__genres.remove(genre)

        except ValueError:
            return


class Review:
    def __init__(self, user: 'User', movie: Movie, review_text: str, rating: int, timestamp: datetime):
        self.__user = user
        self.__movie = movie
        self.__review_text = review_text
        self.__rating = None
        if 1 <= rating <= 10:
            self.__rating = rating
        self.__time = timestamp

    @property
    def user(self) -> 'User':
        return self.__user

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def timestamp(self) -> datetime:
        return self.__time

    def __repr__(self):
        return f"<Review {self.__movie.title}, {self.__time}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.__movie == other.movie and self.__review_text == other.__review_text and \
               self.__rating == other.rating and self.__time == other.timestamp


class User:
    def __init__(self, username: str, password: str):
        if username == "" or type(username) is not str:
            self.__username = None
        else:
            self.__username = username.lower().strip()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password

        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies = 0

    @property
    def user_name(self) -> str:
        return self.__username

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies

    def __repr__(self):
        return f"<User {self.__username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.__username == other.user_name

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.__username < other.user_name

    def __hash__(self):
        return hash(self.__username)

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
            runtime = movie.runtime_minutes
            if runtime is None:
                runtime = 0
            self.__time_spent_watching_movies += runtime

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)


class WatchingQueue:
    def __init__(self):
        self.__movie_queue = []

    def add_to_queue(self, movie: Movie):
        if isinstance(movie, Movie) and movie not in self.__movie_queue:
            self.__movie_queue.append(movie)

    def remove_from_queue(self, movie: Movie):
        if isinstance(movie, Movie) and movie in self.__movie_queue:
            self.__movie_queue.remove(movie)

    def watch_next(self) -> Movie:
        if len(self.__movie_queue) > 0:
            return self.__movie_queue.pop(0)

    def size(self):
        return len(self.__movie_queue)

    def next_in_queue(self):
        if len(self.__movie_queue) > 0:
            return self.__movie_queue[0]


class WatchingSession:
    def __init__(self, host: User, movie: Movie):
        if isinstance(host, User):
            self.__host = host
        else:
            self.__host = None
        self.__friends = []
        if isinstance(movie, Movie):
            self.__watching = movie
        else:
            self.__watching = None

    def add_friend(self, host: User, friend: User):
        if host == self.__host and host is not None:
            if isinstance(friend, User) and friend != self.__host:
                self.__friends.append(friend)

    def kick_user(self, host: User, friend: User):
        if host == self.__host and host is not None:
            if friend in self.__friends:
                self.__friends.remove(friend)

    def change_host(self, old_host: User, new_host: User):
        if old_host == self.__host and isinstance(new_host, User):
            self.__host = new_host
            if self.__host in self.__friends:
                self.__friends.remove(self.__host)

    def change_movie(self, host: User, movie: Movie):
        if host == self.__host and host is not None and isinstance(movie, Movie):
            self.__watching = movie

    def end_session(self, host: User):
        if host == self.__host:
            self.__friends = []
            self.__watching = None

    def users_in_session(self):
        return [self.__host] + self.__friends

    def size(self):
        if self.__host is None:
            return len(self.__friends)
        return len(self.__friends) + 1

    @property
    def watching(self):
        return self.__watching

    @property
    def host(self):
        return self.__host


class WatchList:
    def __init__(self):
        self.__watchlist = []
        self.__iter_index = 0

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie) and movie not in self.__watchlist:
            self.__watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index: int):
        if 0 <= index < len(self.__watchlist):
            return self.__watchlist[index]

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if len(self.__watchlist) > 0:
            return self.__watchlist[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter_index < len(self.__watchlist):
            ret_val = self.__watchlist[self.__iter_index]
            self.__iter_index += 1
            return ret_val
        else:
            self.__iter_index = 0
            raise StopIteration


def make_review(review_text: str, user: User, movie: Movie, rating: int, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, rating, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review
