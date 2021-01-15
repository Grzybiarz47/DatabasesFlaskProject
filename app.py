import os
from flask import Flask, render_template, url_for, request, redirect, session
from connection import Connection
from datetime import datetime

#
#   https://jan-zajda-bd1-projekt.herokuapp.com/
#

app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.secret_key = "projekt"
else:
    app.debug = False
    app.secret_key = os.environ["SECRET_KEY"]

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, must-revalidate"
    return response

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db = Connection()
        ans = db.find_movie_series_game('%' + request.form['mainFindForm'].upper() + '%')
        return render_template('search_results.html', series=ans[0], movies=ans[1], games=ans[2])
        
    else:
        return render_template('index.html')

@app.route('/series/<int:id>', methods=['GET', 'POST'])
def series(id):
    db = Connection()
    ans = db.find_info(table="SERIAL", id_what="id_serial", id=id)
    if request.method == "POST":
        if request.form['submit'] == 'seasons':
            seasons = db.find_seasons(id)
            return render_template('series_all.html', series=ans[0], seasons=seasons)

        elif request.form['submit'] == 'cast':
            cast_series = db.find_cast(table="SERIAL", id_what="id_serial", id=id)
            return render_template('series_all.html', series=ans[0], cast=cast_series)

        elif request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_serial", id)
            return render_template('series_all.html', series=ans[0], prizes=prizes)

        else:
            return "XD"

    else:
        return render_template('series_all.html', series=ans[0])

@app.route('/series/<int:id_serial>/<int:id_sezon>', methods=['GET', 'POST'])
def season(id_serial, id_sezon):
    db = Connection()
    chapters = db.find_chapters(id_sezon)
    ans = db.find_season_info(id_serial, id_sezon)
    return render_template('season_all.html', season=ans[0], chapters=chapters)

@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    db = Connection()
    ans = db.find_info(table="FILM", id_what="id_film", id=id)
    if request.method == "POST":
        if request.form['submit'] == 'cast':
            cast_movie = db.find_cast(table="FILM", id_what="id_film", id=id)
            return render_template('movie_all.html', movie=ans[0], cast=cast_movie)

        elif request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_film", id)
            return render_template('movie_all.html', movie=ans[0], prizes=prizes)

        else:
            return "XD"

    else:
        return render_template('movie_all.html', movie=ans[0])

@app.route('/game/<int:id>', methods=['GET', 'POST'])
def game(id):
    db = Connection()
    ans = db.find_info(table="GRA", id_what="id_gra", id=id)
    if request.method == 'POST':
        if request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_gra", id)
            return render_template('game_all.html', game=ans[0], prizes=prizes)

        else:
            return "XD"

    else:
        return render_template('game_all.html', game=ans[0])

@app.route('/artist/<int:id>', methods=['GET', 'POST'])
def artist(id):
    db = Connection()
    ans = db.find_info(table="ARTYSTA", id_what="id_artysta", id=id)
    prizes = db.find_prizes(id_what="id_artysta", id=id)
    artist_type = db.find_artist_type(id)
    roles = db.find_roles(id)
    return render_template('artist_all.html', artist=ans[0], prizes=prizes, artist_type=artist_type, roles=roles)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/')

    db = Connection()
    message = ""
    if request.method == 'POST':
        log = request.form['login']
        email = request.form['email']
        password = request.form['pass']
        if log and email and password: 
            if db.valid_email_login(email, log):
                if db.register_user({'login': log, 'email': email, 'pass': password, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):
                    message='Rejestracja się powiodła - teraz możesz się zalogować'
                else:
                    message="Błąd przy łączeniu z bazą danych"
            else:
                message='Wystąpił błąd - email lub login znajduje się już w bazie'
        else:
            message='Pola nie mogą być puste'    

    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')

    db = Connection()
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        if email and password:
            if db.login_user({'email': email, 'pass': password}):
                message="Zostałeś zalogowany"
                session['user'] = email
                db.create_observed_view(email)
            else:
                message='Błędne dane'
        else:
            message='Pola nie mogą być puste'

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    db = Connection()
    db.drop_observed_view(session['user'])
    session.pop('user', None)
    return redirect('/')

@app.route('/account', methods=['GET', 'POST'])
def account():
    db = Connection()
    if 'user' in session:
        user_data = db.find_account(session['user'])
        if request.method == 'POST':
            if 'mainFindUserForm' in request.form:
                log = request.form['mainFindUserForm']
                searched_users = db.find_users('%' + log + '%', session['user'])
                observed = db.find_observed(session['user'])
                return render_template('account.html', user_data=user_data[0], observed=observed, searched_users=searched_users)

            elif 'add' in request.form:
                id_obs = request.form['add']
                db.add({'id': id_obs, 'user': session['user'], 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                observed = db.find_observed(session['user'])
                return render_template('account.html', user_data=user_data[0], observed=observed)

            elif 'delete' in request.form:
                id_obs = request.form['delete']
                db.delete({'id': id_obs, 'id_user': db.find_id_user(session['user']), 'user': session['user']})
                observed = db.find_observed(session['user'])
                return render_template('account.html', user_data=user_data[0], observed=observed)

        else:
            observed = db.find_observed(session['user'])
            return render_template('account.html', user_data=user_data[0], observed=observed)
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run()

