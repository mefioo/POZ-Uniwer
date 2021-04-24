from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, PasswordField, DateTimeField, FloatField, widgets
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields.html5 import DateField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.TableWidget()
    option_widget = widgets.CheckboxInput()


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


class Plan(FlaskForm):
    company = SelectField('Placówka', choices=[])
    service = MultiCheckboxField('Rodzaj usługi', choices=[], coerce=int)
    date = DateField('Data', format='%Y-%m-%d')
    time = FloatField('Czas', validators=[DataRequired()])
    submit = SubmitField('Zaplanuj')
