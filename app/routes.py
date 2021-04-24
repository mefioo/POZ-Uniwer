from flask import render_template, url_for, flash, redirect, session
from datetime import timedelta
from functools import wraps
from app import app
from passlib.hash import sha256_crypt
import app.forms as forms
import app.dbconnection as db
import app.helpers as hp


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
    perm = hp.find_rights(session['username'])
    return render_template('main.html', perm=perm, title='Strona główna')


@app.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    perm = hp.find_rights(session['username'])
    form = forms.Plan()
    form = hp.create_service_view(form)
    if form.validate_on_submit():
        hp.add_service_to_db(form)
        flash(f'Pomyślnie dodano nowe zgłoszenie na dzień {form.date.data}.', 'success')
        return redirect('main')
    return render_template('plan.html', perm=perm, form=form, title='Zaplanuj')


@app.route('/orders_list')
@login_required
def orders_list():
    perm = hp.find_rights(session['username'])
    data = hp.create_orders_list_view()
    return render_template('orders_list.html', data=data, perm=perm, title='Wykaz zleceń')


@app.route('/supplies_list')
@login_required
def supplies_list():
    perm = hp.find_rights(session['username'])
    data = hp.create_supplies_list_view()
    return render_template('supplies_list.html', data=data, perm=perm, title='Wykaz zaopatrzenia')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash('Jesteś już zalogowany.', 'danger')
        return redirect(url_for('main'))
    else:
        form = forms.Login()
        if form.validate_on_submit():
            login = form.login.data
            password = str(form.password.data)
            if hp.check_if_login_exists(login):
                rights = db.find_parameter('konta', 'uprawnienia', 'login', login)
                if rights is not 0:
                    userPassword = db.find_parameter('konta', 'haslo', 'login', login)
                    if sha256_crypt.verify(password, userPassword):
                        session['logged_in'] = True
                        session['username'] = login
                        flash(f'Cześć {login}!', 'success')
                        return redirect(url_for('main'))
                else:
                    flash('Aby móc się zalogować musisz posiadać aktywne konto!', 'danger')
                    return redirect(url_for('login'))
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
        login = form.login.data
        if not hp.check_if_login_exists(login):
            password = sha256_crypt.hash(str(form.password.data))
            values = [login, password, form.name.data, form.surname.data]
            db.insert_account(values)
            flash(f'Pomyślnie stworzono konto. Będzie ono aktywne po akceptacji administratora.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Konto o podanym loginie już istnieje.', 'danger')
    return render_template('register.html', form=form, title='Stwórz konto')
