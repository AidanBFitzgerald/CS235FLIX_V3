from datetime import datetime


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self._actor_full_name = None
        else:
            self._actor_full_name = actor_full_name.strip()
        self._colleagues = []
        self._movies = []

    @property
    def actor_full_name(self) -> str:
        return self._actor_full_name

    @property
    def movies(self) -> list:
        return self._movies

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
        if colleague not in self._colleagues and isinstance(colleague, Actor):
            self._colleagues.append(colleague)

    def check_if_this_actor_worked_with(self, colleague):
        if colleague in self._colleagues:
            return True
        return False

    def add_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie) and movie not in self._movies:
            self._movies.append(movie)


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self._director_full_name = None
        else:
            self._director_full_name = director_full_name.strip()
        self._movies = []

    @property
    def director_full_name(self) -> str:
        return self._director_full_name

    @property
    def movies(self) -> list:
        return self._movies

    def __repr__(self):
        return f"<Director {self._director_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        return self.director_full_name == other.director_full_name

    def __lt__(self, other):
        return self.director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.director_full_name)

    def add_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie) and movie not in self._movies:
            self._movies.append(movie)


class Genre:
    def __init__(self, genre_name: str):
        self._movies = []
        if genre_name == "" or type(genre_name) is not str:
            self._genre_name = None
        else:
            self._genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self._genre_name

    @property
    def movies(self) -> list:
        return self._movies

    @movies.setter
    def movies(self, new_movies: list):
        if type(new_movies) is list:
            self._movies = new_movies

    def add_movie(self, movie: 'Movie'):
        if isinstance(movie, Movie) and movie not in self._movies:
            self._movies.append(movie)

    def __repr__(self):
        return f"<Genre {self._genre_name}>"

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

    def __init__(self, title: str, year: int, movie_id: int = None):
        self._description = None
        self._director = None
        self._actors = []
        self._genres = []
        self._runtime_minutes = None
        self._reviews = []
        self._id = movie_id
        self._watchlists = []

        if year >= 1900:
            self._year = year
        else:
            self._year = None
        if title == "" or type(title) is not str:
            self._title = None
        else:
            self._title = title.strip()

        try:
            movie_title = self.title
        except TypeError:
            return

        letter_found = False
        self._first_letter = movie_title[0]

        for letter in movie_title:
            if 65 <= ord(letter) <= 90:
                self._first_letter = letter
                letter_found = True
                break
        for letter in movie_title:
            if letter_found:
                break
            if 48 <= ord(letter) <= 57:
                self._first_letter = letter
                letter_found = True
                break

    @property
    def id(self):
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def year(self) -> int:
        return self._year

    @property
    def description(self) -> str:
        return self._description

    @property
    def director(self) -> Director:
        return self._director

    @property
    def actors(self) -> list:
        return self._actors

    @property
    def genres(self) -> list:
        return self._genres

    @property
    def runtime_minutes(self) -> int:
        return self._runtime_minutes

    @property
    def reviews(self):
        return self._reviews

    @property
    def first_letter(self):
        return self._first_letter

    @property
    def watchlists(self):
        return self._watchlists

    @title.setter
    def title(self, new_title: str):
        if new_title == "" or type(new_title) is not str:
            self._title = None
        else:
            self._title = new_title.strip()

    @description.setter
    def description(self, new_description: str):
        if new_description == "" or type(new_description) is not str:
            self._description = None
        else:
            self._description = new_description.strip()

    @director.setter
    def director(self, new_director: Director):
        if isinstance(new_director, Director):
            self._director = new_director

    @actors.setter
    def actors(self, new_actors: list):
        if type(new_actors) is list:
            self._actors = new_actors

    @genres.setter
    def genres(self, new_genres):
        if type(new_genres) is list:
            self._genres = new_genres

    @runtime_minutes.setter
    def runtime_minutes(self, new_runtime: int):
        if type(new_runtime) is int:
            if new_runtime <= 0:
                raise ValueError
            self._runtime_minutes = new_runtime

    @reviews.setter
    def reviews(self, new_reviews):
        if type(new_reviews) is list:
            self._reviews = new_reviews

    def add_review(self, review: 'Review'):
        if type(review) is Review:
            self._reviews.append(review)

    def get_first_letter(self):
        return self._first_letter

    def add_watchlist(self, watchlist: 'User'):
        if isinstance(watchlist, WatchList):
            self._watchlists.append(watchlist)

    def remove_watchlist(self, watchlist: 'User'):
        if watchlist in self._watchlists:
            self._watchlists.remove(watchlist)

    def __repr__(self):
        return f"<Movie {self._title}, {self._year}>"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self._title == other._title and self._year == other._year

    def __lt__(self, other):
        if isinstance(other, Movie):
            index_this_title = self.title.find(self.get_first_letter())
            index_other_title = other.title.find(other.get_first_letter())
            this_title = self._title[index_this_title:]
            other_title = other.title[index_other_title:]
            if self._title == other.title:
                return self._year < other._year
            else:
                return this_title < other_title
        return False

    def __hash__(self):
        return hash((self._title, self._year))

    def add_actor(self, actor: Actor):
        if isinstance(actor, Actor) and actor not in self._actors:
            self._actors.append(actor)

    def remove_actor(self, actor):
        try:
            self._actors.remove(actor)

        except ValueError:
            return

    def add_genre(self, genre):
        if isinstance(genre, Genre) and genre not in self._genres:
            self._genres.append(genre)

    def remove_genre(self, genre):
        try:
            self._genres.remove(genre)

        except ValueError:
            return


class Review:
    def __init__(self, user: 'User', movie: Movie, review_text: str, rating: int, timestamp: datetime):
        self._user = user
        self._movie = movie
        self._review_text = review_text
        self._rating = None
        if 1 <= rating <= 10:
            self._rating = rating
        self._time = timestamp

    @property
    def user(self) -> 'User':
        return self._user

    @property
    def movie(self) -> Movie:
        return self._movie

    @property
    def review_text(self) -> str:
        return self._review_text

    @property
    def rating(self) -> int:
        return self._rating

    @property
    def timestamp(self) -> datetime:
        return self._time

    def __repr__(self):
        return f"<Review {self._movie.title}, {self._time}>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self._movie == other.movie and self._review_text == other._review_text and \
               self._rating == other.rating and self._time == other.timestamp


class User:
    def __init__(self, username: str, password: str):
        if username == "" or type(username) is not str:
            self._username = None
        else:
            self._username = username.lower().strip()
        if password == "" or type(password) is not str:
            self._password = None
        else:
            self._password = password

        self._watched_movies = []
        self._reviews = []
        self._time_spent_watching_movies = 0
        self._watchlist = []

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def watched_movies(self) -> list:
        return self._watched_movies

    @property
    def reviews(self) -> list:
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self._time_spent_watching_movies

    @property
    def watchlist(self):
        return self._watchlist

    def add_to_watchlist(self, movie: Movie):
        watchlist = WatchList(self)
        watchlist.watchlist = self._watchlist
        watchlist.add_movie(movie)
        self._watchlist = watchlist.watchlist

    def remove_from_watchlist(self, movie: Movie):
        watchlist = WatchList(self)
        watchlist.watchlist = self._watchlist
        watchlist.remove_movie(movie)
        self._watchlist = watchlist.watchlist

    def __repr__(self):
        return f"<User {self._username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self._username == other.username

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self._username < other.username

    def __hash__(self):
        return hash(self._username)

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            if movie not in self._watched_movies:
                self._watched_movies.append(movie)
            runtime = movie.runtime_minutes
            if runtime is None:
                runtime = 0
            self._time_spent_watching_movies += runtime

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self._reviews.append(review)


class WatchingQueue:
    def __init__(self):
        self._movie_queue = []

    def add_to_queue(self, movie: Movie):
        if isinstance(movie, Movie) and movie not in self._movie_queue:
            self._movie_queue.append(movie)

    def remove_from_queue(self, movie: Movie):
        if isinstance(movie, Movie) and movie in self._movie_queue:
            self._movie_queue.remove(movie)

    def watch_next(self) -> Movie:
        if len(self._movie_queue) > 0:
            return self._movie_queue.pop(0)

    def size(self):
        return len(self._movie_queue)

    def next_in_queue(self):
        if len(self._movie_queue) > 0:
            return self._movie_queue[0]


class WatchingSession:
    def __init__(self, host: User, movie: Movie):
        if isinstance(host, User):
            self._host = host
        else:
            self._host = None
        self._friends = []
        if isinstance(movie, Movie):
            self._watching = movie
        else:
            self._watching = None

    def add_friend(self, host: User, friend: User):
        if host == self._host and host is not None:
            if isinstance(friend, User) and friend != self._host:
                self._friends.append(friend)

    def kick_user(self, host: User, friend: User):
        if host == self._host and host is not None:
            if friend in self._friends:
                self._friends.remove(friend)

    def change_host(self, old_host: User, new_host: User):
        if old_host == self._host and isinstance(new_host, User):
            self._host = new_host
            if self._host in self._friends:
                self._friends.remove(self._host)

    def change_movie(self, host: User, movie: Movie):
        if host == self._host and host is not None and isinstance(movie, Movie):
            self._watching = movie

    def end_session(self, host: User):
        if host == self._host:
            self._friends = []
            self._watching = None

    def users_in_session(self):
        return [self._host] + self._friends

    def size(self):
        if self._host is None:
            return len(self._friends)
        return len(self._friends) + 1

    @property
    def watching(self):
        return self._watching

    @property
    def host(self):
        return self._host


class WatchList:
    def __init__(self, user: User):
        self._watchlist = []
        self._iter_index = 0
        self._user = user

    @property
    def watchlist(self):
        return self._watchlist

    @watchlist.setter
    def watchlist(self, new_list):
        self._watchlist = new_list

    def add_movie(self, movie: Movie):
        if isinstance(movie, Movie) and movie not in self._watchlist:
            movie.add_watchlist(self._user)
            self._watchlist.append(movie)

    def remove_movie(self, movie: Movie):
        if movie in self._watchlist:
            movie.remove_watchlist(self._user)

    def select_movie_to_watch(self, index: int):
        if 0 <= index < len(self._watchlist):
            return self._watchlist[index]

    def size(self):
        return len(self._watchlist)

    def first_movie_in_watchlist(self):
        if len(self._watchlist) > 0:
            return self._watchlist[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self._iter_index < len(self._watchlist):
            ret_val = self._watchlist[self._iter_index]
            self._iter_index += 1
            return ret_val
        else:
            self._iter_index = 0
            raise StopIteration


def make_review(review_text: str, user: User, movie: Movie, rating: int,
                timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, rating, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review
