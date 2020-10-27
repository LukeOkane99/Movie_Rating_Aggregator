import sqlite3
import get_ratings

movie = 'tenet'
year = '2020'
imdb, metacritic = get_ratings.get_imdb_metacritic_ratings(movie, year)
tomatometer, audience_score = get_ratings.get_rotten_tomatoes_ratings(movie, year)
letterboxd= get_ratings.get_letterboxd_rating(movie, year)
tmdb = get_ratings.get_tmdb_rating(movie, year)
average = get_ratings.get_average_rating(imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb)

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
    try:
        with sqlite3.connect('database.db') as conn:
            conn.cursor().execute("INSERT INTO Movies (title, year, Imdb_rating, Metascore, Tomatometer, Audience_score, Letterboxd_rating, Tmdb_rating, Average_rating) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ttl, yr, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average))

            conn.commit()
            print("record added successfully")
    except:
        # undo insertion if issues
        conn.rollback()
        print("error when inserting movie record")
    finally:
        conn.close()

#create_database()
add_movie_to_db(movie, year, imdb, metacritic, tomatometer, audience_score, letterboxd, tmdb, average)

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM Movies")
    rows = cur.fetchall()

    for row in rows:
        print(row)