from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Regexp
from .models import Users

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
    ])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Create a Username', validators=[
        DataRequired(message="Username is required"),
    ])
    password = PasswordField('Create a Password', validators=[
        DataRequired(message="Password is required"),
    ])
    email = EmailField('Enter your email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        # In the code, there's no email field in the Users model
        pass