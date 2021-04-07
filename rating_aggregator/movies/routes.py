import flask
from flask import render_template, url_for, flash, request, redirect, abort, Blueprint, current_app
from rating_aggregator import db, bcrypt, mail
from rating_aggregator.models import User, Movie, WatchlistMovies
from rating_aggregator.get_ratings import get_all_ratings
from sqlalchemy import desc, asc, func
from rating_aggregator.users.forms import registrationForm, loginForm, UpdateDetailsForm, RequestResetForm, ResetPasswordForm
from rating_aggregator.movies.forms import TitleSearchForm, ResultsSearchForm, YearSearchForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

movies = Blueprint('movies', __name__)

#<------------Movie Endpoints------------->

# Route to access all movies in the database
@movies.route('/', methods=['GET', 'POST'])
@movies.route('/movies/all', methods=['GET', 'POST'])
def get_all_movies():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))
    movies = Movie.query.order_by(Movie.title).all()
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('all_movies.html', title='All Movies', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)

# Route displaying searched movie results
@movies.route('/movies/results/<name>', defaults={'year': None}, methods=['GET', 'POST'])
@movies.route('/movies/results/<name>_<year>',methods=['GET', 'POST'])
def title_results(name, year):
    search_form = TitleSearchForm()
    results_form = ResultsSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))
    elif flask.request.method == 'POST' and results_form.validate_on_submit():
        return redirect(url_for('movies.search_for_movie', name=results_form.result_movie_title.data.lower().strip(), year=results_form.result_movie_year.data.strip()))
    count = 0
    movies = Movie.query.filter(func.lower(Movie.title).like("%{0}%".format(name.lower()))).order_by(Movie.title).all()
    watchlist_entries = []
    for movie in movies:
        count += 1
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('results.html', title='Results', movies=movies, search_form=search_form, results_form=results_form, count=count, name=name, year=year, watchlist_entries=watchlist_entries)

# Route to return specific movie
@movies.route('/movies/<name>_<year>', methods=['GET', 'POST'])
def search_for_movie(name, year):
    search_form = TitleSearchForm()
    results_form = ResultsSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))
    elif flask.request.method == 'GET':
        watchlist_entry = None
        movie = Movie.query.filter(func.lower(Movie.title) == name.lower()).filter_by(year = year).first()
        if movie:
            if current_user.is_authenticated:
                watchlist_entry = WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first()
            return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=movie.movie_image, watchlist_entry=watchlist_entry)
        else:
            try:
                ttl, yr, imdb, imdb_votes, metacritic, metacritic_votes, synopsis, imdb_url, metacritic_url, tomatometer, tomatometer_votes, audience, audience_votes, rotten_tomatoes_url, letterboxd, letterboxd_votes, letterboxd_url, tmdb, tmdb_votes, image, tmdb_url, avg = get_all_ratings(name, year)
                movie = Movie(title=ttl, year=yr, imdb_rating=imdb, imdb_votes=imdb_votes, imdb_url=imdb_url, metascore=metacritic, metascore_votes=metacritic_votes, metacritic_url=metacritic_url, tomatometer=tomatometer,
                    tomatometer_votes=tomatometer_votes, audience_score=audience, audience_score_votes=audience_votes, rotten_tomatoes_url=rotten_tomatoes_url, letterboxd_rating=letterboxd, letterboxd_votes=letterboxd_votes,
                     letterboxd_url=letterboxd_url, tmdb_rating=tmdb, tmdb_votes=tmdb_votes, tmdb_url=tmdb_url, average_rating=avg, movie_image=image, synopsis=synopsis)
                db.session.add(movie)
                db.session.commit()
                return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=movie.movie_image)
            except Exception as e:
                db.session.rollback()
                return redirect(url_for('movies.title_results', name=name, year=year))

# Route to search for a movie by year 
@movies.route('/movies/year', methods=['GET', 'POST'])
@movies.route('/movies/year/<year>', methods=['GET', 'POST'])
def search_movies_by_year(year=None):
    search_form = TitleSearchForm()
    year_form = YearSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))
    if flask.request.method == 'POST' and year_form.validate_on_submit():
        return redirect(url_for('movies.search_movies_by_year', year=year_form.movie_year.data.strip()))
    count = 0
    movies = Movie.query.filter_by(year=year).order_by(Movie.title).all()
    watchlist_entries = []
    for movie in movies:
        count += 1
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('get_movie_by_year.html', title='Movies by year', movies=movies, search_form=search_form, year_form=year_form, year=year, count=count, watchlist_entries=watchlist_entries)

# Route to display movies based on high to low ratings
@movies.route('/movies/hightolow', methods=['GET', 'POST'])
def get_high_to_low_ratings():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('get_hightolow_ratings.html', title='High to Low Ratings', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)

# Route to display movies based on low to high ratings
@movies.route('/movies/lowtohigh', methods=['GET', 'POST'])
def get_low_to_high_ratings():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = Movie.query.order_by(asc(Movie.average_rating)).all()
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('get_lowtohigh_ratings.html', title='Low to High Ratings', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)

# Route to display favourable movies
@movies.route('/movies/favourable', methods=['GET', 'POST'])
def get_favourable_reviews():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = Movie.query.filter(Movie.average_rating >= 60).order_by(Movie.title).all()
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('get_favourable_movies.html', title='Favourable Ratings', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)

# Route to display non-favourable reviews
@movies.route('/movies/non-favourable', methods=['GET', 'POST'])
def get_nonfavourable_reviews():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = Movie.query.filter(Movie.average_rating < 60).order_by(Movie.title).all()
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('get_non-favourable_movies.html', title='Non-Favourable Ratings', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)

# Route to display top 10 movies
@movies.route('/movies/top10', methods=['GET', 'POST'])
def get_top10_movies():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    movies = movies[:10]
    watchlist_entries = []
    for movie in movies:
        if current_user.is_authenticated:
            if WatchlistMovies.query.filter_by(userId=current_user.id, movieId=movie.movieId).first():
                watchlist_entries.append(movie)
    return render_template('top_10_movies.html', title='Top 10 Movies', movies=movies, search_form=search_form, watchlist_entries=watchlist_entries)