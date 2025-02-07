from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.validators import ValidationError
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
import sqlalchemy
from app import db
from app.models import User

class LoginForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        
        user = db.session.scalar(sqlalchemy.select(User).where(
            User.username == username.data))
    
    def validate_email(self, email):
        
        user = db.session.scalar(sqlalchemy.select(User).where(
            User.email == email.data))
        
        if user is not None:
            
            raise ValidationError('Please use a different email address.')