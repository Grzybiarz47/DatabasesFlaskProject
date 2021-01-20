from flask import Blueprint, render_template, session, request
from connection import Connection
from functions import add_comment, add_grade

list_data = Blueprint('list_data', __name__, static_folder='static', template_folder='templates')

##################################
#    ARTIST GAME SERIES MOVIE    #
##################################
@list_data.route('/series/<int:id>', methods=['GET', 'POST'])
def series(id):
    db = Connection()
    ans = db.find_info(table='SERIAL', id_what='id_serial', id=id)
    grade = db.find_grade(table='SERIAL', id_what='id_serial', id=id)
    if 'user' in session:
        grade['ocena_uzytkownika'] = db.find_user_grade(table='SERIAL', id_what='id_serial', id=id, id_user=db.find_id_user(session['user']))['ocena']

    if request.method == 'POST':
        task = request.form['submit']
        if task == 'seasons':
            seasons = db.call_procedure("projekt.wyszukaj_sezony(%s)" % (id))
            return render_template('series_all.html', series=ans, grade=grade, seasons=seasons)

        elif task == 'cast':
            cast_series = db.find_cast(table='SERIAL', id_what='id_serial', id=id)
            return render_template('series_all.html', series=ans, grade=grade, cast=cast_series)

        elif task == 'prize':
            prizes = db.find_prizes(id_what='id_serial', id=id)
            return render_template('series_all.html', series=ans, grade=grade, prizes=prizes)

        elif task == 'comments':
            comments = db.find_comments(table='SERIAL', email=session['user'], id_what='id_serial', id=id)    
            return render_template('series_all.html', series=ans, grade=grade, comments=comments)

        elif task == 'add_comment':
            message = add_comment(table='SERIAL', id_what='id_serial', id=id, com=request.form['comments_area'])
            return render_template('series_all.html', series=ans, grade=grade, message=message)

        elif task == 'add_grade':
            message = add_grade(table='SERIAL', id_what='id_serial', id=id, grade=request.form['select_grade'])
            grade = db.find_grade(table='SERIAL', id_what='id_serial', id=id)
            grade['ocena_uzytkownika'] = request.form['select_grade']
            return render_template('series_all.html', series=ans, grade=grade, message=message)

    else:
        return render_template('series_all.html', series=ans, grade=grade)

@list_data.route('/series/<int:id_serial>/<int:id_sezon>', methods=['GET', 'POST'])
def season(id_serial, id_sezon):
    db = Connection()
    chapters = db.call_procedure("projekt.wyszukaj_odcinki(%s)" % (id_sezon))
    season = db.call_procedure("projekt.wyszukaj_info_sezon(%s, %s)" % (id_serial, id_sezon))[0]
    return render_template('season_all.html', season=season, chapters=chapters)

@list_data.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    db = Connection()
    ans = db.find_info(table='FILM', id_what='id_film', id=id)
    grade = db.find_grade(table='FILM', id_what='id_film', id=id)
    if 'user' in session:
        grade['ocena_uzytkownika'] = db.find_user_grade(table='FILM', id_what='id_film', id=id, id_user=db.find_id_user(session['user']))['ocena']

    if request.method == 'POST':
        task = request.form['submit']
        if task == 'cast':
            cast_movie = db.find_cast(table='FILM', id_what='id_film', id=id)
            return render_template('movie_all.html', movie=ans, grade=grade, cast=cast_movie)

        elif task == 'prize':
            prizes = db.find_prizes(id_what='id_film', id=id)
            return render_template('movie_all.html', movie=ans, grade=grade, prizes=prizes)

        elif task == 'comments':
            comments = db.find_comments(table='FILM', email=session['user'], id_what='id_film', id=id)    
            return render_template('movie_all.html', movie=ans, grade=grade, comments=comments)

        elif task == 'add_comment':
            message = add_comment(table='FILM', id_what='id_film', id=id, com=request.form['comments_area'])
            return render_template('movie_all.html', movie=ans, grade=grade, message=message)

        elif task == 'add_grade':
            message = add_grade(table='FILM', id_what='id_film', id=id, grade=request.form['select_grade'])
            grade = db.find_grade(table='FILM', id_what='id_film', id=id)
            grade['ocena_uzytkownika'] = request.form['select_grade']
            return render_template('movie_all.html', movie=ans, grade=grade, message=message)

    else:
        return render_template('movie_all.html', movie=ans, grade=grade)

@list_data.route('/game/<int:id>', methods=['GET', 'POST'])
def game(id):
    db = Connection()
    ans = db.find_info(table='GRA', id_what='id_gra', id=id)
    grade = db.find_grade(table='GRA', id_what='id_gra', id=id)
    if 'user' in session:
        grade['ocena_uzytkownika'] = db.find_user_grade(table='GRA', id_what='id_gra', id=id, id_user=db.find_id_user(session['user']))['ocena']

    if request.method == 'POST':
        task = request.form['submit']
        if task == 'prize':
            prizes = db.find_prizes(id_what='id_gra', id=id)
            return render_template('game_all.html', game=ans, grade=grade, prizes=prizes)

        elif task == 'comments':
            comments = db.find_comments(table='GRA', email=session['user'], id_what='id_gra', id=id)    
            return render_template('game_all.html', game=ans, grade=grade, comments=comments)

        elif task == 'add_comment':
            message = add_comment(table='GRA', id_what='id_gra', id=id, com=request.form['comments_area'])
            return render_template('game_all.html', game=ans, grade=grade, message=message)

        elif task == 'add_grade':
            message = add_grade(table='GRA', id_what='id_gra', id=id, grade=request.form['select_grade'])
            grade = db.find_grade(table='GRA', id_what='id_gra', id=id)
            grade['ocena_uzytkownika'] = request.form['select_grade']
            return render_template('game_all.html', game=ans, grade=grade, message=message)

    else:
        return render_template('game_all.html', game=ans, grade=grade)

@list_data.route('/artist/<int:id>', methods=['GET', 'POST'])
def artist(id):
    db = Connection()
    ans = db.find_info(table='ARTYSTA', id_what='id_artysta', id=id)
    prizes = db.find_prizes(id_what='id_artysta', id=id)
    #artist_type = db.find_artist_type(id)
    artist_type = db.call_procedure("projekt.wyszukaj_rodzaj_artystów(%s)" % (id))
    roles = db.call_procedure("projekt.wyszukaj_role(%s)" % (id))
    return render_template('artist_all.html', artist=ans, prizes=prizes, artist_type=artist_type, roles=roles)