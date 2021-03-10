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

main = Blueprint('main', __name__)

# Route for help page
@main.route('/help', methods=['GET', 'POST'])
def help():
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower().strip()))
    return render_template('help.html', title='Help', search_form=search_form)

#<--------------------Error Handling------------------->

"""
# Route for 403 custom error page
@main.errorhandler(403)
def forbidden_page(e):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    return render_template('403.html', title='403', search_form=search_form), 403

# Route for 404 custom error page
@main.errorhandler(404)
def not_found_page(e):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('title_results', name=search_form.movie_title.data.lower()))

    return render_template('404.html', title='404', search_form=search_form), 404
"""