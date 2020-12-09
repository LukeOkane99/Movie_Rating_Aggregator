import flask
from flask import render_template, url_for, flash, request
from rating_aggregator import app, db
from rating_aggregator.models import User, Movie, WatchlistMovies
from rating_aggregator.get_ratings import get_all_ratings

# Route for index page
@app.route('/', methods=['GET'])
@app.route('/index')
def hello():
    return render_template('index.html')

# Endpoint to access all movies in the database
@app.route('/movies/all', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    return render_template('all_movies.html', title='All Movies', movies=movies)

# Endpoint to search for a specific movie
@app.route('/movies/<title>&<year>', methods=['GET', 'POST'])
def search_for_movie(title, year):
    movie = Movie.query.filter_by(title=title, year=year).first()
    if flask.request.method == 'POST':
        if movie:
            return 'Movie already exists in database!'
        else:
            try:
                ttl, yr, imdb, metacritic, synopsis, image, letterboxd, tomatometer, audience, tmdb, avg = get_all_ratings(title, year)
                movie = Movie(title=ttl, year=yr, imdb_rating=imdb, metascore=metacritic, tomatometer=tomatometer, audience_score=audience, letterboxd_rating=letterboxd,
                 tmdb_rating=tmdb, average_rating=avg, movie_image=image, synopsis=synopsis)
                db.session.add(movie)
                db.session.commit()
                print("Movie successfully added!")
            except:
                db.session.rollback()
                print("error when inserting movie record")
            finally:
                db.session.close()
                return 'Connection closed!'
    elif flask.request.method == 'GET':
        return render_template('get_movie.html', title='Searched Movie', movie=movie)

