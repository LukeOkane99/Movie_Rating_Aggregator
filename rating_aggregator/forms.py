from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Registration form so new user can post their details
class registrationForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])
    email_address = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    register_button = SubmitField('Register')

# Login form so registered users can log in to the application
class loginForm(FlaskForm):
    email_address = StringField('Enter Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    login_button = SubmitField('Login')
