import flask
from flask import render_template, url_for, flash, request
from rating_aggregator import app, db
from rating_aggregator.models import User, Movie, WatchlistMovies
from rating_aggregator.get_ratings import get_all_ratings
from sqlalchemy import desc, asc

# Route for index page
@app.route('/', methods=['GET'])
@app.route('/index')
def hello():
    return render_template('index.html')

#<------------Movie Endpoints------------->

# Route to access all movies in the database
@app.route('/movies/all', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    return render_template('all_movies.html', title='All Movies', movies=movies)

# Route to search for a specific movie
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
            except:
                db.session.rollback()
            finally:
                db.session.close()
                return 'Connection closed!'
    elif flask.request.method == 'GET':
        return render_template('get_movie.html', title='Searched Movie', movie=movie)

# Route to search for a movie by year
@app.route('/movies/<year>', methods=['GET', 'POST'])
def search_movies_by_year(year):
    movies = Movie.query.filter_by(year=year).all()
    if movies:
        return render_template('get_movie_by_year.html', title='Movies by year', movies=movies)
    else:
        return 'There are no movies stored for this year!'

# Route to display movies based on high to low ratings
@app.route('/movies/hightolow', methods=['GET'])
def get_high_to_low_ratings():
    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    return render_template('get_hightolow_ratings.html', title='High to Low Ratings', movies=movies)

# Route to display movies based on low to high ratings
@app.route('/movies/lowtohigh', methods=['GET'])
def get_low_to_high_ratings():
    movies = Movie.query.order_by(asc(Movie.average_rating)).all()
    return render_template('get_lowtohigh_ratings.html', title='Low to High Ratings', movies=movies)

# Route to display favourable movies
@app.route('/movies/favourable', methods=['GET'])
def get_favourable_reviews():
    movies = Movie.query.filter(Movie.average_rating >= 70).all()
    return render_template('get_favourable_movies.html', title='Favourable Ratings', movies=movies)

# Route to display non-favourable reviews
@app.route('/movies/non-favourable', methods=['GET'])
def get_nonfavourable_reviews():
    movies = Movie.query.filter(Movie.average_rating <= 69).all()
    return render_template('get_non-favourable_movies.html', title='Non-Favourable Ratings', movies=movies)

#<--------------------User Endpoints------------------->

