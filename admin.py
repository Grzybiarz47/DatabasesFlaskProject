from flask import Blueprint, render_template, redirect, session, request, url_for
from connection import Connection
from datetime import datetime
import json

admin = Blueprint('admin', __name__, static_folder='static', template_folder='templates')

##################################
#              ADMIN             #
##################################
@admin.route('/')
def admin_menu():
    if 'user' in session:
        return render_template('admin_menu.html', message=request.args.get('message'))
    else:
        return redirect('/')

@admin.route('/movie', methods=['GET', 'POST'])
def add_movie():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            name = form['name'].strip().upper()
            desc = form['desc']
            prod = form['prod']
            box_off = form['box_off']
            studio = form['studio']
            db = Connection()
            if name:
                if prod:
                    db.call_insert_procedure("projekt.dodaj_film('%s', '%s', '%s', '%s', %s)" % (name, desc, box_off, studio, prod))
                else:
                    db.call_insert_procedure("projekt.dodaj_film('%s', '%s', '%s', '%s')" % (name, desc, box_off, studio))
                return redirect(url_for('admin.admin_menu', message='Dodano film do bazy danych'))
            else:
                return redirect(url_for('admin.admin_menu', message='Nie udało się dodać filmu do bazy'))
        else:
            return render_template('movie_form.html')
    else:
        return redirect('/')

@admin.route('/game', methods=['GET', 'POST'])
def add_game():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            name = form['name'].strip().upper()
            desc = form['desc']
            prod = form['prod']
            sales = form['sales'] + 'mln'
            studio = form['studio']
            db = Connection()
            if name:
                if prod:
                    db.call_insert_procedure("projekt.dodaj_grę('%s', '%s', '%s', '%s', %s)" % (name, desc, sales, studio, prod))
                else:
                    db.call_insert_procedure("projekt.dodaj_grę('%s', '%s', '%s', '%s', %s)" % (name, desc, sales, studio))
                return redirect(url_for('admin.admin_menu', message='Dodano grę do bazy danych'))
            else:
                return redirect(url_for('admin.admin_menu', message='Nie udało się dodać gry do bazy'))
        else:
            return render_template('game_form.html')
    else:
        return redirect('/')

@admin.route('/series', methods=['GET', 'POST'])
def add_series():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            name = form['name'].strip().upper()
            desc = form['desc']
            prod = form['prod']
            db = Connection()
            if name:
                id_season = -1
                if prod:
                    id_series = db.call_insert_procedure("projekt.dodaj_serial('%s', '%s', %s)" % (name, desc, prod))
                else:
                    id_series = db.call_insert_procedure("projekt.dodaj_serial('%s', '%s')" % (name, desc))
                seasons = form['seasons']
                for i in range(1, int(seasons) + 1):
                    prod = form['season_' + str(i) + '_prod']
                    id_season = -1
                    if prod:
                        id_season = db.call_insert_procedure("projekt.dodaj_sezon(%s, %s)" % (id_series, prod))
                    else:
                        id_season = db.call_insert_procedure("projekt.dodaj_sezon(%s)" % (id_series))
                    chapters = form['season_' + str(i)]
                    for j in range(1, int(chapters) + 1):
                        db.call_insert_procedure("projekt.dodaj_odcinek(%s, '%s')" % (id_season, form['chapter_' + str(i) + '_' + str(j)]))
                return redirect(url_for('admin.admin_menu', message='Dodano serial do bazy danych'))

            return redirect(url_for('admin.admin_menu', message='Nie udało się dodać serialu do bazy'))
        else:
            return render_template('series_form.html')
    else:
        return redirect('/')

@admin.route('/prize', methods=['GET', 'POST'])
def add_prize():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            name = form['name']
            year = form['year']
            if not year:
                year = -1
            db = Connection()
            if name:
                fname = form['fname']
                lname = form['lname']
                game = form['game'].upper()
                movie = form['movie'].upper()
                series = form['series'].upper()
                if db.call_insert_procedure("projekt.dodaj_nagrodę('%s', %s, '%s', '%s', '%s', '%s', '%s')" % (name, year, movie, series, game, fname, lname)):
                    return redirect(url_for('admin.admin_menu', message='Dodano nagrodę do bazy danych'))

            return redirect(url_for('admin.admin_menu', message='Nie udało się dodać nagrody do bazy'))
        else:
            return render_template('prize_form.html')
    else:
        return redirect('/')
    
@admin.route('/artist', methods=['GET', 'POST'])
def add_artist():
    if 'user' in session:
        if request.method == 'POST':
            form = request.form
            db = Connection()
            fname = form['fname'].strip()
            lname = form['lname'].strip()
            birth = form['birth']
            if not birth:
                birth = -1
            death = form['death']
            if not death:
                death = -1
            db = Connection()
            if fname and lname:
                id_artist = db.call_insert_procedure("projekt.dodaj_artystę('%s', '%s', %s, %s)" % (fname, lname, birth, death))
                if 'on' in form.getlist('actor'):
                    db.call_insert_procedure("projekt.dodaj_typ_artysty(%s, '%s')" % (id_artist, 'aktor'))
                if 'on' in form.getlist('director'):
                    db.call_insert_procedure("projekt.dodaj_typ_artysty(%s, '%s')" % (id_artist, 'reżyser'))
                if 'on' in form.getlist('producer'):
                    db.call_insert_procedure("projekt.dodaj_typ_artysty(%s, '%s')" % (id_artist, 'producent'))
                if 'on' in form.getlist('screenwriter'):
                    db.call_insert_procedure("projekt.dodaj_typ_artysty(%s, '%s')" % (id_artist, 'scenarzysta'))
                counter = 1
                while(('ms_' + str(counter)) in form):
                    ms = form['ms_' + str(counter)].upper()
                    role = form['role_' + str(counter)]
                    character = form['character_' + str(counter)]
                    db.call_insert_procedure("projekt.dodaj_obsadę('%s', '%s', '%s', %s)" % (ms, role, character, id_artist))
                    print("projekt.dodaj_obsadę('%s', '%s', '%s', %s)" % (ms, role, character, id_artist))
                    counter += 1
                return redirect(url_for('admin.admin_menu', message='Dodano artystę do bazy danych'))

            return redirect(url_for('admin.admin_menu', message='Nie udało się dodać artysty do bazy'))
        else:
            return render_template('artist_form.html')
    else:
        return redirect('/')