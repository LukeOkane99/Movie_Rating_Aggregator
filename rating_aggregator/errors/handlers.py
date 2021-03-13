import flask
from flask import Blueprint, render_template, request, redirect, url_for
from rating_aggregator.movies.forms import TitleSearchForm

errors = Blueprint('errors', __name__)

#<--------------------Error Handling------------------->

# Route for 403 custom error page
@errors.app_errorhandler(403)
def forbidden_page(error):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower()))

    return render_template('403.html', title='403', search_form=search_form), 403

# Route for 404 custom error page
@errors.app_errorhandler(404)
def not_found_page(error):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower()))

    return render_template('404.html', title='404', search_form=search_form), 404

@errors.app_errorhandler(500)
def general_error(error):
    search_form = TitleSearchForm()
    if flask.request.method == 'POST' and search_form.validate_on_submit():
        return redirect(url_for('movies.title_results', name=search_form.movie_title.data.lower()))

    return render_template('500.html', title='500', search_form=search_form), 500