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
from rating_aggregator.users.utils import send_reset_email

users = Blueprint('users', __name__)

#<--------------------User Endpoints------------------->

# Route to register a new user
@users.route('/register', methods=['GET', 'POST'])
def register():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!', 'danger')
        return redirect(url_for('movies.get_all_movies'))

    register_form = registrationForm()
    if register_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(forename=register_form.forename.data, surname=register_form.surname.data.strip(), email=register_form.email.data.strip(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account successfully created. You can now log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register an account', register_form=register_form, search_form=search_form)

# Route to login a registered user
@users.route('/login', methods=['GET', 'POST'])
def login():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!', 'danger')
        return redirect(url_for('movies.get_all_movies'))
    else:
        login_form = loginForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, login_form.password.data): # check if both hashed passwords are equal
                login_user(user)
                # access page user was trying to access before login
                next_page = request.args.get('next')
                flash('Login successful!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('movies.get_all_movies'))
            else:
                flash('Login unsuccessful, please check you have input the correct email and password!', 'danger')
    return render_template('login.html', title='Log in to your account', login_form=login_form, search_form=search_form)

# Route to log user out
@users.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('User successfully logged out', 'success')
    return redirect(url_for('movies.get_all_movies'))

# Route to view user's profile
@users.route('/users/<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    update_form = UpdateDetailsForm()
    if current_user.is_authenticated:
        if current_user.admin:
            user = User.query.filter_by(id=user_id).first()
            if update_form.validate_on_submit():
                user.forename = update_form.forename.data.strip()
                user.surname = update_form.surname.data.strip()
                if update_form.email.data.strip() != user.email:
                    other_user = User.query.filter_by(email=update_form.email.data).first()
                    if other_user:
                        flash('This email is in use, please use a different one!', 'danger')
                    else:
                        user.email = update_form.email.data.strip()
                        db.session.commit()
                        flash('Account details successfully updated!', 'success')
                else:
                    db.session.commit()
                    flash('Account details successfully updated!', 'success')
                return redirect(url_for('users.profile', user_id=user.id))
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
                flash('Account details successfully updated!', 'success')
                return redirect(url_for('users.profile', user_id=current_user.id))
            elif request.method == 'GET':
                # Populate form with users current details
                update_form.forename.data = current_user.forename
                update_form.surname.data = current_user.surname
                update_form.email.data = current_user.email
    else:
        abort(403)

    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    return render_template('profile.html', title='Profile', search_form=search_form, update_form=update_form)

# Route to request password reset
@users.route('/reset_password', methods=['GET', 'POST'])
def request_reset():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!', 'danger')
        return redirect(url_for('movies.get_all_movies'))
    reset_form = RequestResetForm()
    if reset_form.validate_on_submit():
        user = User.query.filter_by(email=reset_form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'success')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', title='Reset Password', search_form=search_form, reset_form=reset_form)

# Route to reset password with acquired token
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    if current_user.is_authenticated:
        flash('You are already logged in with a registered account!', 'danger')
        return redirect(url_for('movies.get_all_movies'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This is an invalid or expired token', 'danger')
        return redirect(url_for('users.request_reset'))
    password_reset_form = ResetPasswordForm()
    if password_reset_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(password_reset_form.password.data).decode('utf-8')
        user.password =  hashed_password
        db.session.commit()
        flash('Your password has been successfully updated. You can now log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', search_form=search_form, password_reset_form=password_reset_form)

#<--------------------User Watchlist------------------->

# Route to view user's watchlist
@users.route('/users/<user_id>/watchlist', methods=['GET', 'POST'])
@login_required
def get_watchlist(user_id):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    movies = []

    watchlist = WatchlistMovies.query.filter_by(userId=current_user.id).all()
    for entry in watchlist:
        movie = Movie.query.filter_by(movieId=entry.movieId).first()
        movies.append(movie)
    return render_template('watchlist.html', title='Watchlist', search_form=search_form, movies=movies)

# Route to add a movie to watchlist
@users.route('/users/<user_id>/watchlist/add/movies/<movie_id>/<name>_<year>', methods=['POST'])
@login_required
def add_to_watchlist(user_id, movie_id, name, year):
    movie = WatchlistMovies.query.filter_by(userId=user_id, movieId=movie_id).first()
    if movie:
        flash('Movie already exists in watchlist!', 'danger')
        return redirect(request.referrer)
    else:
        movie = WatchlistMovies(userId=user_id, movieId=movie_id)
        db.session.add(movie)
        db.session.commit()
        flash('Movie added to watchlist!', 'success')
        return redirect(request.referrer)

# Route to delete a movie from watchlist
@users.route('/users/<user_id>/watchlist/delete/movies/<movie_id>/<name>_<year>', methods=['POST'])
@login_required
def delete_from_watchlist(user_id, movie_id, name, year):
    watchlist_entry = WatchlistMovies.query.filter_by(userId=user_id, movieId=movie_id).first()
    db.session.delete(watchlist_entry)
    db.session.commit()
    flash('Movie removed from watchlist!', 'success')
    return redirect(request.referrer)
    
#<--------------------Admin Endpoints------------------->

# Route to view all users
@users.route('/users/all', methods=['GET', 'POST'])
@login_required
def get_all_users():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))

    users = User.query.order_by(User.id).all()

    if current_user.admin:
        return render_template('all_users.html', title='All users', search_form=search_form, users=users)
    else: 
        abort(403)

# Route to add or remove user admin priviledges
@users.route('/users/<user_id>/admin=<admin>', methods=['POST'])
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
            flash('User admin priviledges successfully updated!', 'success')
        except:
            db.session.rollback()
        finally:
            return redirect(url_for('users.get_all_users'))

# Route to delete a user account
@users.route('/users/<user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User account has been deleted!', 'success')
    return redirect(url_for('users.get_all_users'))