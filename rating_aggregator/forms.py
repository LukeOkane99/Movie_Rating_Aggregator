from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rating_aggregator.models import User, Movie

# Registration form so new user can post their details
class registrationForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    register_button = SubmitField('Register')

    # check if inputted email already exists in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is in use, please use a different one!')

# Login form so registered users can log in to the application
class loginForm(FlaskForm):
    email = StringField('Enter Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    login_button = SubmitField('Login')

# Form to search for a movie in the header
class MovieSearchForm(FlaskForm):
    movie_title = StringField('Search Title', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Title"})
    movie_year = StringField('Search Year', validators=[DataRequired()], render_kw={"placeholder": "Search Movie Year"})
    submit_button = SubmitField('Search')

# Form to search for movies by year
class YearSearchForm(FlaskForm):
    year = StringField('Search by Year', validators=[DataRequired()])

# Form so users can update their account details
class UpdateDetailsForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    update_button = SubmitField('Update Details')

    # check if updated email is already in use by another user
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is in use, please use a different one!')
    