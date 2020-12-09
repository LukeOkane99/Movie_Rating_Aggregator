from rating_aggregator import app, db
from models import User, Movie, WatchlistMovies
import get_ratings

movie = 'inception'
release_year = '2010'
title, release_year, imdb, metacritic, synopsis, image, letterboxd, tomatometer, audience, tmdb, avg = get_all_ratings(movie, year)

# create database if it doesn't already exist
def create_db():
    if db is None:
        db.create_all()
    else:
        print('The database already exists')

# add a new movie to the database if not present
def add_movie_to_db(ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average, image, synopsis):
    record = Movie.query.filter_by(title=ttl).first()
    if record:
        print("Record already exists!")
    else:
        try:
            movie = Movie(ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average, image, synopsis)
            db.session.add(movie)
            db.session.commit()
        except:
            db.session.rollback()
            print("error when inserting movie record")
        finally:
            session.close()
            print("Movie successfully added!")

add_movie_to_db(title, release_year, imdb, metacritic, synopsis, image, letterboxd, tomatometer, audience, tmdb, avg)

"""
# add a new movie to the database if not present
def add_movie_to_db(ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average, image, synopsis):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        # Check if movie record already exists in database
        cur.execute('SELECT rowid FROM Movies WHERE Title = (?) AND Year = (?)', (ttl,yr))
        record = cur.fetchall()
        if (len(record) != 0):
            print("A record already exists for this Movie")
        else:
            try:
                cur.execute('INSERT INTO Movies (title, year, Imdb_rating, Metascore, Tomatometer, Audience_score, Letterboxd_rating, Tmdb_rating, Average_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average))
                conn.commit()
            except:
                # undo insertion if issues
                conn.rollback()
                print("error when inserting movie record")
            finally:
                if conn:
                    print("record added successfully")

# delete all movie records from Movies table
def delete_all_movies():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM Movies')
        conn.commit()

# show all records in Movies table
def get_all_movies():
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM Movies")
        rows = cur.fetchall()
        return rows

def get_movie(ttl, yr):
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM Movies WHERE Title = (?) AND Year = (?)', (ttl,yr))
        record = cur.fetchall()
        if (len(record) != 0):
            print("Record found")
            return record[0]
        else:
            print("No record exists for this movie")
"""