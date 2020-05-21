from flask_wtf import FlaskForm
from wtforms import MultipleFileField, PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo, Email, Length

class ImageForm(FlaskForm):
    files = MultipleFileField('Images to Upload')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired('Please Input Something')])

class RegisterForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(message='Invalid Email'), InputRequired('Please Input Something')])
    password = PasswordField('Password', validators=[InputRequired('Please Input Something'), Length(min=6, message='Password Must Be longer than 6 characters')])
    confirm = PasswordField('Confirm password', validators=[EqualTo('password', message='Passwords do not match')])

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[Email(message='Invalid Email'), InputRequired('Please Input Something')])
    password = PasswordField('Password', validators=[InputRequired('Please Input Something')])
