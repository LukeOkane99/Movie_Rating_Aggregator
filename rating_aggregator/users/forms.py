from flask import request
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from rating_aggregator.models import User

# Registration form so new user can post their details
class registrationForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Enter Your Forename.."})
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)], render_kw={"placeholder": "Enter Your Surname.."})
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "Enter Your Email.."})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password.."})
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your Password.."})
    register_button = SubmitField('Register')

    # check if inputted email already exists in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is in use, please use a different one!')

# Login form so registered users can log in to the application
class loginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "Enter Your Email.."})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your password.."})
    login_button = SubmitField('Login')

# Form so users can update their account details
class UpdateDetailsForm(FlaskForm):
    forename = StringField('Forename', validators=[DataRequired(), Length(min=2, max=30)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    update_button = SubmitField('Update Details')
    pass

    # check if updated email is already in use by another user
    def validate_email(self, email):
        if not current_user.admin:
            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('This email is in use, please use a different one!')

# Form for reset request page
class RequestResetForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)], render_kw={"placeholder": "Enter Your Email.."})
    request_reset_button = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account linked to this email. Please make sure you are registered!')

# Form for password reset page
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Your Password.."})
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your Password.."})
    password_reset_button = SubmitField('Reset Password')