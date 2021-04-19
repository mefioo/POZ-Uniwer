from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, PasswordField, TextField
from wtforms.validators import DataRequired, Length, EqualTo


class Login(FlaskForm):
    login = StringField('Login', validators=[DataRequired("Musisz podać login.")])
    password = PasswordField('Hasło', validators=[DataRequired("Musisz podać hasło.")])
    submit = SubmitField('Zaloguj')


class Register(FlaskForm):
    login = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password_confirmation = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Imię', validators=[DataRequired(), Length(max=20)])
    surname = StringField('Nazwisko', validators=[DataRequired(), Length(max=30)])
    submit = SubmitField('Stwórz')
