import flask
from flask import render_template, url_for, flash, request, redirect
from rating_aggregator import app, db, bcrypt
from rating_aggregator.models import User, Movie, WatchlistMovies
from rating_aggregator.get_ratings import get_all_ratings
from sqlalchemy import desc, asc, func
from rating_aggregator.forms import registrationForm, loginForm, MovieSearchForm
from flask_login import login_user, current_user, logout_user

# Route for index page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(name=None, year=None):
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))
    return render_template('index.html', search_form=search_form)

#<------------Movie Endpoints------------->

# Route to access all movies in the database
@app.route('/movies/all', methods=['GET', 'POST'])
def get_all_movies():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))
    movies = Movie.query.all()
    return render_template('all_movies.html', title='All Movies', movies=movies, search_form=search_form)

# Route to search for a specific movie
@app.route('/movies/<name>_<year>', methods=['GET', 'POST'])
def search_for_movie(name, year):
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))
    movie = Movie.query.filter(func.lower(Movie.title) == name.lower()).filter_by(year = year).first()
    if movie:
        image = movie.movie_image
        return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=image)
    else:
        try:
            ttl, yr, imdb, metacritic, synopsis, image, letterboxd, tomatometer, audience, tmdb, avg = get_all_ratings(name, year)
            movie = Movie(title=ttl, year=yr, imdb_rating=imdb, metascore=metacritic, tomatometer=tomatometer, audience_score=audience, letterboxd_rating=letterboxd,
                tmdb_rating=tmdb, average_rating=avg, movie_image=image, synopsis=synopsis)
            db.session.add(movie)
            db.session.commit()
            image=movie.movie_image
        except:
            db.session.rollback()
            return 'No such Movie could be found'
        finally:
            return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=image)
    return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=image)

# Route to search for a movie by year
@app.route('/movies/<year>', methods=['GET', 'POST'])
def search_movies_by_year(year):
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))
    movies = Movie.query.filter_by(year=year).all()

    if movies:
        return render_template('get_movie_by_year.html', title='Movies by year', movies=movies, search_form=search_form)
    else:
        return 'There are no movies stored for this year!'

# Route to display movies based on high to low ratings
@app.route('/movies/hightolow', methods=['GET', 'POST'])
def get_high_to_low_ratings():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    return render_template('get_hightolow_ratings.html', title='High to Low Ratings', movies=movies, search_form=search_form)

# Route to display movies based on low to high ratings
@app.route('/movies/lowtohigh', methods=['GET', 'POST'])
def get_low_to_high_ratings():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    movies = Movie.query.order_by(asc(Movie.average_rating)).all()
    return render_template('get_lowtohigh_ratings.html', title='Low to High Ratings', movies=movies, search_form=search_form)

# Route to display favourable movies
@app.route('/movies/favourable', methods=['GET', 'POST'])
def get_favourable_reviews():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    movies = Movie.query.filter(Movie.average_rating >= 60).all()
    return render_template('get_favourable_movies.html', title='Favourable Ratings', movies=movies, search_form=search_form)

# Route to display non-favourable reviews
@app.route('/movies/non-favourable', methods=['GET', 'POST'])
def get_nonfavourable_reviews():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    movies = Movie.query.filter(Movie.average_rating <= 59).all()
    return render_template('get_non-favourable_movies.html', title='Non-Favourable Ratings', movies=movies, search_form=search_form)

# Route to display top 10 movies
@app.route('/movies/top10', methods=['GET', 'POST'])
def get_top10_movies():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    movie_list = []
    for movie in movies[:10]:
        movie_list.append(movie)
    return render_template('top_10_movies.html', title='Top 10 Movies', movie_list=movie_list, search_form=search_form)


#<--------------------User Endpoints------------------->

# Route to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!')
        return redirect(url_for('index'))

    register_form = registrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(forename=register_form.forename.data, surname=register_form.surname.data, email=register_form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been successfully created. You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register an account', register_form=register_form, search_form=search_form)

# Route to login a registered user
@app.route('/login', methods=['GET', 'POST'])
def login():
    search_form = MovieSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=search_form.movie_title.data.lower(), year=search_form.movie_year.data))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!')
        return redirect(url_for('index'))

    login_form = loginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data): # check if both hashed passwords are equal
            login_user(user)
            flash('Login was successful!')
            return redirect(url_for('index'))
        else:
            flash('Login was unsuccessful. Please check you have input the correct email and password', 'danger')
    return render_template('login.html', title='Log in to your account', login_form=login_form, search_form=search_form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('User successfully logged out')
    return redirect(url_for('index'))
#<--------------------Admin Endpoints------------------->
