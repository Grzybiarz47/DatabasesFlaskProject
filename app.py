from flask import Flask, render_template, request
from loginout import loginout
from list_data import list_data
from account import account
from stats import stats
from admin import admin
from connection import Connection
import os

#
#   https://jan-zajda-bd1-projekt.herokuapp.com/
#

app = Flask(__name__)
app.register_blueprint(loginout, url_prefix='')
app.register_blueprint(list_data, url_prefix='')
app.register_blueprint(account, url_prefix='')
app.register_blueprint(stats, url_prefix='')
app.register_blueprint(admin, url_prefix='/admin')

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.secret_key = 'projekt'
else:
    app.debug = False
    app.secret_key = os.environ['SECRET_KEY']

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db = Connection()
        query = '%' + request.form['mainFindForm'].upper() + '%'
        series = db.call_procedure("projekt.wyszukaj_seriale('%s')" % (query))
        movies = db.call_procedure("projekt.wyszukaj_filmy('%s')" % (query))
        games = db.call_procedure("projekt.wyszukaj_gry('%s')" % (query))
        return render_template('search_results.html', series=series, movies=movies, games=games)
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()

