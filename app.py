from flask import Flask, render_template, url_for, request, redirect
from connection import DatabaseFind

#
#   https://jan-zajda-bd1-projekt.herokuapp.com/
#

app = Flask(__name__)
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db = DatabaseFind()
        ans = db.find_movie_series_game('%' + request.form['mainFindForm'].upper() + '%')
        db.close()
        return render_template('search_results.html', series=ans[0], movies=ans[1], games=ans[2])
        
    else:
        return render_template('index.html')

@app.route('/series/<int:id>', methods=['GET', 'POST'])
def series(id):
    db = DatabaseFind()
    ans = db.find_info(table="SERIAL", id_what="id_serial", id=id)
    if request.method == "POST":
        if request.form['submit'] == 'seasons':
            seasons = db.find_seasons(id)
            db.close()
            return render_template('series_all.html', series=ans[0], seasons=seasons)

        elif request.form['submit'] == 'cast':
            cast_series = db.find_cast(table="SERIAL", id_what="id_serial", id=id)
            db.close()
            return render_template('series_all.html', series=ans[0], cast=cast_series)
            return "A"

        elif request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_serial", id)
            db.close()
            return render_template('series_all.html', series=ans[0], prizes=prizes)

        else:
            return "XD"

    else:
        db.close()
        return render_template('series_all.html', series=ans[0])

@app.route('/series/<int:id_serial>/<int:id_sezon>', methods=['GET', 'POST'])
def season(id_serial, id_sezon):
    db = DatabaseFind()
    chapters = db.find_chapters(id_sezon)
    ans = db.find_season_info(id_serial, id_sezon)
    db.close()
    return render_template('season_all.html', season=ans[0], chapters=chapters)

@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    db = DatabaseFind()
    ans = db.find_info(table="FILM", id_what="id_film", id=id)
    if request.method == "POST":
        if request.form['submit'] == 'cast':
            cast_movie = db.find_cast(table="FILM", id_what="id_film", id=id)
            db.close()
            return render_template('movie_all.html', movie=ans[0], cast=cast_movie)

        elif request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_film", id)
            db.close()
            return render_template('movie_all.html', movie=ans[0], prizes=prizes)

        else:
            db.close()
            return "XD"

    else:
        db.close()
        return render_template('movie_all.html', movie=ans[0])

@app.route('/game/<int:id>', methods=['GET', 'POST'])
def game(id):
    db = DatabaseFind()
    ans = db.find_info(table="GRA", id_what="id_gra", id=id)
    if request.method == 'POST':
        if request.form['submit'] == 'prize':
            prizes = db.find_prizes("id_gra", id)
            db.close()
            return render_template('game_all.html', game=ans[0], prizes=prizes)

        else:
            db.close()
            return "XD"

    else:
        db.close()
        return render_template('game_all.html', game=ans[0])

@app.route('/artist/<int:id>', methods=['GET', 'POST'])
def artist(id):
    db = DatabaseFind()
    ans = db.find_info(table="ARTYSTA", id_what="id_artysta", id=id)
    prizes = db.find_prizes(id_what="id_artysta", id=id)
    artist_type = db.find_artist_type(id)
    roles = db.find_roles(id)
    db.close()
    return render_template('artist_all.html', artist=ans[0], prizes=prizes, artist_type=artist_type, roles=roles)

if __name__ == "__main__":
    app.run()

