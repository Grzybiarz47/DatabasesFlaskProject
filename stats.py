from flask import Blueprint, render_template
from connection import Connection

stats = Blueprint('stats', __name__, static_folder='static', template_folder='templates')

##################################
#           STATISTICS           #
##################################
@stats.route('/stats')
def show_stats():
    db = Connection()
    all = db.call_procedure("projekt.statystyki_ogólne")[0]
    artist_type = db.call_procedure("projekt.statystyki_typy_artystów")
    best_stats = db.call_procedure("projekt.statystyki_najwyższe_oceny")
    return render_template('stats.html', all=all, artist_type=artist_type, best_stats=best_stats)