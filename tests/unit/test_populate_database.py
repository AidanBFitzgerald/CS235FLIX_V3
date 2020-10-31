from sqlalchemy import inspect, select

from flix.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['actors', 'directors', 'genres', 'movie_actors', 'movie_genres', 'movies',
                                           'reviews', 'users', 'watchlist_movies']


def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_tag_names = []
        for row in result:
            all_tag_names.append(row['name'])

        assert all_tag_names == ['Action', 'Adventure', 'Sci-Fi', 'Mystery', 'Horror', 'Thriller', 'Animation',
                                 'Comedy', 'Family', 'Fantasy', 'Drama', 'Music', 'Biography', 'Romance', 'History',
                                 'Crime', 'Western', 'War', 'Musical', 'Sport']


def test_database_populate_select_all_movies(database_engine):
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table movies
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []

        for row in result:
            all_movies.append((row['id'], row['title']))

        num_movies = len(all_movies)
        assert num_movies == 1000

        assert all_movies[0] == (1, 'Guardians of the Galaxy')
        assert all_movies[num_movies//2] == (501, 'Maze Runner: The Scorch Trials')
        assert all_movies[num_movies-1] == (1000, 'Nine Lives')



def test_database_populate_select_all_directors(database_engine):
    inspector = inspect(database_engine)
    name_of_directors_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:

        select_statement = select([metadata.tables[name_of_directors_table]])
        result = connection.execute(select_statement)

        all_directors = []

        for row in result:
            all_directors.append(row['fullname'])

    num_directors = len(all_directors)
    assert all_directors[0] == 'James Gunn'
    assert all_directors[num_directors//2] == 'Jon S. Baird'
    assert all_directors[num_directors-1] == 'Scot Armstrong'


def test_database_populate_select_all_actors(database_engine):
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_actors_table]])
        result = connection.execute(select_statement)

        all_actors = []

        for row in result:
            all_actors.append(row['fullname'])

        num_actors = len(all_actors)

        assert all_actors[0] == 'Chris Pratt'
        assert all_actors[num_actors//2] == 'Mickey Rourke'
        assert all_actors[num_actors-1] == 'Cheryl Hines'
