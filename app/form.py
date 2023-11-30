from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import  InputRequired,Length,Email,DataRequired
from werkzeug.security import generate_password_hash,check_password_hash

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Ricorda l\'accesso')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ContactForm(FlaskForm):
    nomeC = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    telefono = StringField('Numero di Telefono',validators=[DataRequired()])
    email_body = StringField('Messaggio',validators=[DataRequired()])

