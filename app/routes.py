from flask import render_template, url_for, flash, redirect, session
from datetime import timedelta
from functools import wraps
from app import app
import app.forms as forms
import app.dbconnection as db

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("By uzyskać dostęp do tej strony musisz być zalogowany.", "danger")
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def default():
    if 'logged_in' in session:
        return redirect(url_for('main'))
    return redirect('login')


@app.route('/main')
@login_required
def main():
    return render_template('main.html', title='Strona główna')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Jesteś już zalogowany.', 'danger')
        return redirect(url_for('main'))
    else:
        form = forms.Login()
        if form.validate_on_submit():
            actPassword = 'macadams'
            password = form.password.data
            actLogin = 'macadams'
            login = form.login.data
            if password == actPassword and login == actLogin:
                session['logged_in'] = True
                session['username'] = login
                flash(f'Cześć {login}!', 'success')
                return redirect(url_for('main'))
            else:
                flash('Błędny login lub hasło. Spróbuj ponownie.', 'danger')
    return render_template('login.html', form=form, title='Zaloguj')


@app.route('/logout')
@login_required
def logout():
    username = session['username']
    session.clear()
    flash(f"Do zobaczenia {username}!", "success")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.Register()
    if form.validate_on_submit():
        flash(f'Pomyślnie stworzono konto. Będzie ono aktywne po akceptacji administratora.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Stwórz konto')
