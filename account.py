from flask import Blueprint, render_template, redirect, session, request
from connection import Connection
from datetime import datetime

account = Blueprint('account', __name__, static_folder='static', template_folder='templates')

##################################
#          ACCOUNT MENU          #
##################################
@account.route('/account', methods=['GET', 'POST'])
def show_account():
    db = Connection()
    if 'user' in session:
        user_data = db.call_procedure("projekt.wyszukaj_info_użytkownika('%s')" % (session['user']))[0]
        if request.method == 'POST':
            if 'mainFindUserForm' in request.form:
                log = request.form['mainFindUserForm']
                searched_users = db.call_procedure("projekt.wyszukaj_użytkowników('%s', '%s')" % (session['user'], '%' + log + '%'))
                observed = db.call_procedure("projekt.wyszukaj_obserwowanych('%s')" % (session['user']))
                return render_template('account.html', user_data=user_data, observed=observed, searched_users=searched_users)

            elif 'add' in request.form:
                id_obs = request.form['add']
                db.add_to_observed({'id': id_obs, 'user': session['user'], 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                observed = db.call_procedure("projekt.wyszukaj_obserwowanych('%s')" % (session['user']))
                return render_template('account.html', user_data=user_data, observed=observed)

            elif 'delete' in request.form:
                id_obs = request.form['delete']
                db.delete_from_observed({'id': id_obs, 'id_user': db.call_procedure("projekt.id_użytkownika('%s')" % (session['user']))[0]['id_użytkownika'], 'user': session['user']})
                observed = db.call_procedure("projekt.wyszukaj_obserwowanych('%s')" % (session['user']))
                return render_template('account.html', user_data=user_data, observed=observed)

        else:
            observed = db.call_procedure("projekt.wyszukaj_obserwowanych('%s')" % (session['user']))
            return render_template('account.html', user_data=user_data, observed=observed)
    else:
        return redirect('/')