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
            name = form['name'].upper()
            desc = form['desc']
            prod = form['prod']
            box_off = form['box_off']
            studio = form['studio']
            if not prod:
                prod = -1
            db = Connection()
            if name and db.add_movie({'name':name, 'desc':desc, 'prod':prod, 'box_off':box_off, 'studio':studio}):
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
            name = form['name'].upper()
            desc = form['desc']
            prod = form['prod']
            if not prod:
                prod = -1
            sales = form['sales'] + 'mln'
            studio = form['studio']
            db = Connection()
            if name and db.add_game({'name':name, 'desc':desc, 'prod':prod, 'sales':sales, 'studio':studio}):
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
            name = form['name'].upper()
            desc = form['desc']
            prod = form['prod']
            if not prod:
                prod = -1
            db = Connection()
            if name:
                id_series = db.add_series({'name':name, 'desc':desc, 'prod':prod})
                seasons = form['seasons']
                for i in range(1, int(seasons) + 1):
                    id_season = db.add_season({'id_series': id_series, 'prod':form['season_' + str(i) + '_prod']})
                    chapters = form['season_' + str(i)]
                    for j in range(1, int(chapters) + 1):
                        db.add_chapter({'id_season': id_season, 'name': form['chapter_' + str(i) + '_' + str(j)]})
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
            fname = form['fname']
            lname = form['lname']
            birth = form['birth']
            if not birth:
                birth = -1
            death = form['death']
            if not death:
                death = -1
            db = Connection()
            if fname and lname:
                id_artist = db.add_artist({'fname': fname, 'lname': lname, 'birth': birth, 'death': death})
                if 'on' in form.getlist('actor'):
                    db.add_type({'id_artist': id_artist, 'type': 'aktor'})
                if 'on' in form.getlist('director'):
                    db.add_type({'id_artist': id_artist, 'type': 'reżyser'})
                if 'on' in form.getlist('producer'):
                    db.add_type({'id_artist': id_artist, 'type': 'producent'})
                if 'on' in form.getlist('screenwriter'):
                    db.add_type({'id_artist': id_artist, 'type': 'scenarzysta'})
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