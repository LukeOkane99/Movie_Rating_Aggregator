import flask
from flask import render_template, url_for, flash, request, redirect, abort
from rating_aggregator import app, db, bcrypt
from rating_aggregator.models import User, Movie, WatchlistMovies
from rating_aggregator.get_ratings import get_all_ratings
from sqlalchemy import desc, asc, func
from rating_aggregator.forms import registrationForm, loginForm, TitleSearchForm, UpdateDetailsForm, ResultsSearchForm, YearSearchForm
from flask_login import login_user, current_user, logout_user, login_required

# Route for index page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))
    return render_template('index.html', search_form=search_form)

#<------------Movie Endpoints------------->

# Route to access all movies in the database
@app.route('/movies/all', methods=['GET', 'POST'])
def get_all_movies():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))
    movies = Movie.query.order_by(Movie.title).all()
    return render_template('all_movies.html', title='All Movies', movies=movies, search_form=search_form)

# Route displaying searched movie results
@app.route('/movies/results/<name>', methods=['GET', 'POST'])
def title_results(name):
    search_form = TitleSearchForm()
    results_form = ResultsSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))
    elif flask.request.method == 'POST' and results_form.validate_on_submit():
        return redirect(url_for('search_for_movie', name=results_form.result_movie_title.data.lower(), year=results_form.result_movie_year.data))
    count = 0
    movies = Movie.query.filter(func.lower(Movie.title).like("%{0}%".format(name.lower()))).all()
    for movie in movies:
        count += 1
    return render_template('results.html', title='Results', movies=movies, search_form=search_form, results_form=results_form, count=count, name=name)

# Route to return specific movie
@app.route('/movies/<name>_<year>', methods=['GET', 'POST'])
def search_for_movie(name, year):
    search_form = TitleSearchForm()
    results_form = ResultsSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))
    elif flask.request.method == 'GET':
        movie = Movie.query.filter(func.lower(Movie.title) == name.lower()).filter_by(year = year).first()
        if movie:
            return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=movie.movie_image)
        else:
            try:
                ttl, yr, imdb, metacritic, synopsis, tomatometer, audience, letterboxd, tmdb, image, avg = get_all_ratings(name, year)
                movie = Movie(title=ttl, year=yr, imdb_rating=imdb, metascore=metacritic, tomatometer=tomatometer, audience_score=audience, letterboxd_rating=letterboxd,
                    tmdb_rating=tmdb, average_rating=avg, movie_image=image, synopsis=synopsis)
                db.session.add(movie)
                db.session.commit()
                return render_template('get_movie.html', title='Searched Movie', movie=movie, search_form=search_form, image=movie.movie_image)
            except Exception as e:
                db.session.rollback()
                abort(404)

# Route to search for a movie by year ***** TODO *****
@app.route('/movies/year', methods=['GET', 'POST'])
@app.route('/movies/year/<year>', methods=['GET', 'POST'])
def search_movies_by_year(year=None):
    search_form = TitleSearchForm()
    year_form = YearSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))
    if flask.request.method == 'POST' and year_form.validate_on_submit():
        return redirect(url_for('search_movies_by_year', year=year_form.movie_year.data))

    movies = Movie.query.filter_by(year=year).all()
    return render_template('get_movie_by_year.html', title='Movies by year', movies=movies, search_form=search_form, year_form=year_form, year=year)

# Route to display movies based on high to low ratings
@app.route('/movies/hightolow', methods=['GET', 'POST'])
def get_high_to_low_ratings():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    return render_template('get_hightolow_ratings.html', title='High to Low Ratings', movies=movies, search_form=search_form)

# Route to display movies based on low to high ratings
@app.route('/movies/lowtohigh', methods=['GET', 'POST'])
def get_low_to_high_ratings():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = Movie.query.order_by(asc(Movie.average_rating)).all()
    return render_template('get_lowtohigh_ratings.html', title='Low to High Ratings', movies=movies, search_form=search_form)

# Route to display favourable movies
@app.route('/movies/favourable', methods=['GET', 'POST'])
def get_favourable_reviews():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = Movie.query.filter(Movie.average_rating >= 60).all()
    return render_template('get_favourable_movies.html', title='Favourable Ratings', movies=movies, search_form=search_form)

# Route to display non-favourable reviews
@app.route('/movies/non-favourable', methods=['GET', 'POST'])
def get_nonfavourable_reviews():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = Movie.query.filter(Movie.average_rating <= 59).all()
    return render_template('get_non-favourable_movies.html', title='Non-Favourable Ratings', movies=movies, search_form=search_form)

# Route to display top 10 movies
@app.route('/movies/top10', methods=['GET', 'POST'])
def get_top10_movies():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = Movie.query.order_by(desc(Movie.average_rating)).all()
    movie_list = []
    for movie in movies[:10]:
        movie_list.append(movie)
    return render_template('top_10_movies.html', title='Top 10 Movies', movie_list=movie_list, search_form=search_form)


#<--------------------User Endpoints------------------->

# Route to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

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
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!')
        return redirect(url_for('index'))

    login_form = loginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data): # check if both hashed passwords are equal
            login_user(user)
            # access page user was trying to access before login
            next_page = request.args.get('next')
            flash('Login was successful!')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login was unsuccessful. Please check you have input the correct email and password', 'danger')
    return render_template('login.html', title='Log in to your account', login_form=login_form, search_form=search_form)

# Route to log user out
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('User successfully logged out')
    return redirect(url_for('index'))

# Route to view user's profile
@app.route('/users/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    update_form = UpdateDetailsForm()
    if current_user.is_authenticated:
        if current_user.admin:
            user = User.query.filter_by(id=user_id).first()
            if update_form.validate_on_submit():
                user.forename = update_form.forename.data
                user.surname = update_form.surname.data
                if update_form.email.data != user.email:
                    other_user = User.query.filter_by(email=update_form.email.data).first()
                    if other_user:
                        flash('This email is already taken, please provide another!')
                else:
                    user.email = update_form.email.data
                    db.session.commit()
                    flash('Account details successfully updated!')
                    return redirect(url_for('profile', user_id=user.id))
            elif request.method == 'GET':
                # Populate form with users current details
                update_form.forename.data = user.forename
                update_form.surname.data = user.surname
                update_form.email.data = user.email
        elif not current_user.admin:
            if update_form.validate_on_submit():
                current_user.forename = update_form.forename.data
                current_user.surname = update_form.surname.data
                current_user.email = update_form.email.data
                db.session.commit()
                flash('Account details successfully updated!')
                return redirect(url_for('profile', user_id=current_user.id))
            elif request.method == 'GET':
                # Populate form with users current details
                update_form.forename.data = current_user.forename
                update_form.surname.data = current_user.surname
                update_form.email.data = current_user.email
    else:
        abort(403)

    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    return render_template('profile.html', title='Profile', search_form=search_form, update_form=update_form)

#<--------------------User Watchlist------------------->

# Route to view user's watchlist
@app.route('/users/<user_id>/watchlist', methods=['GET', 'POST'])
@login_required
def get_watchlist(user_id):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    movies = []

    watchlist = WatchlistMovies.query.filter_by(userId=current_user.id).all()
    for entry in watchlist:
        movie = Movie.query.filter_by(movieId=entry.movieId).first()
        movies.append(movie)
        
    return render_template('watchlist.html', title='Watchlist', search_form=search_form, movies=movies)

# Route to add a movie to watchlist
@app.route('/users/<user_id>/watchlist/add/movies/<movie_id>/<name>_<year>', methods=['POST'])
@login_required
def add_to_watchlist(user_id, movie_id, name, year):
    movie = WatchlistMovies.query.filter_by(userId=user_id, movieId=movie_id).first()
    if movie:
        flash('Movie already exists in watchlist!')
        return redirect(url_for('search_for_movie', name=name, year=year))
    else:
        movie = WatchlistMovies(userId=user_id, movieId=movie_id)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added to watchlist!')
        return redirect(url_for('search_for_movie', name=name, year=year))

# Route to delete a movie from watchlist
@app.route('/users/<user_id>/watchlist/delete/movies/<movie_id>/<name>_<year>', methods=['POST'])
@login_required
def delete_from_watchlist(user_id, movie_id, name, year):
    watchlist_entry = WatchlistMovies.query.filter_by(userId=user_id, movieId=movie_id).first()
    db.session.delete(watchlist_entry)
    db.session.commit()
    flash('Movie removed from watchlist!')
    return redirect(url_for('get_watchlist', user_id=user_id))
    
#<--------------------Admin Endpoints------------------->

# Route to view all users
@app.route('/users/all', methods=['GET', 'POST'])
@login_required
def get_all_users():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    users = User.query.order_by(User.id).all()

    if current_user.admin:
        return render_template('all_users.html', title='All users', search_form=search_form, users=users)
    else: 
        abort(403)

# Route to add or remove user admin priviledges
@app.route('/users/<user_id>/admin=<admin>', methods=['POST'])
@login_required
def update_admin_role(user_id, admin):
    if current_user.admin:
        try:
            user = User.query.filter_by(id=user_id).first()
            if user.admin:
                user.admin = False
            else:
                user.admin = True
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            return redirect(url_for('get_all_users'))

# Route to delete a user account
@app.route('/users/<user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User account has been deleted!')
    return redirect(url_for('get_all_users'))

#<--------------------Error Handling------------------->

# Route for 403 custom error page
@app.errorhandler(403)
def forbidden_page(e):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    return render_template('403.html', title='403', search_form=search_form), 403

# Route for 404 custom error page
@app.errorhandler(404)
def not_found_page(e):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    return render_template('404.html', title='404', search_form=search_form), 404
    