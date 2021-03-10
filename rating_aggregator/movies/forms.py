from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from rating_aggregator.models import Movie

# Form to search for movie title
class TitleSearchForm(FlaskForm):
    movie_title = StringField('Search Title', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Title"})
    submit_button = SubmitField('')

# Form to get exact search for movie on results page
class ResultsSearchForm(FlaskForm):
    result_movie_title = StringField('Search Title', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Title"})
    result_movie_year = StringField('Search Year', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Year"})
    submit = SubmitField('Search')

# Form to search for movies by year
class YearSearchForm(FlaskForm):
    movie_year = StringField('Search by Year', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Year"})
    submit_year = SubmitField('Search')