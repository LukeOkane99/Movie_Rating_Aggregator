import sqlite3
import get_ratings

movie = 'Bob'
release_year = '2005'
#title, year, imdb, metascore, tomatometer, audience_score, letterboxd, tmdb, avg = get_ratings.get_all_ratings(movie, release_year)

# create database if it doesn't already exist
def create_db():
    # create and connect to database
    conn = sqlite3.connect('database.db')
    # create movies table
    conn.execute('CREATE TABLE Movies (MovieId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Title TEXT NOT NULL, Year TEXT NOT NULL, Imdb_rating REAL, Metascore REAL, Tomatometer REAL, Audience_score REAL, Letterboxd_rating REAL, Tmdb_rating REAL, Average_rating REAL)')
    # create users table
    conn.execute('CREATE TABLE Users (UserId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Forename TEXT NOT NULL, Surname TEXT NOT NULL, Username TEXT NOT NULL, Password TEXT NOT NULL, Date_created TEXT NOT NULL)')
    conn.close()

# add a new movie to the database if not present
def add_movie_to_db(ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average):
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