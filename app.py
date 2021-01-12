from flask import Flask, render_template, url_for, request, redirect
from connection import DatabaseConnection

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
        db = DatabaseConnection()
        ans = db.find_movie_series_game('%' + request.form['mainFindForm'].upper() + '%')
        db.close()
        return render_template('search_results.html', series=ans[0], movies=ans[1], games=ans[2])
    else:
        return render_template('index.html')

@app.route('/series/<int:id>', methods=['GET', 'POST'])
def series(id):
    return 'XD'

@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie(id):
    return 'XD'

@app.route('/game/<int:id>', methods=['GET', 'POST'])
def game(id):
    return 'XD'

if __name__ == "__main__":
    app.run()

