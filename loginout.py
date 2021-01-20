from flask import Blueprint, render_template, session, request, redirect
from connection import Connection
from datetime import datetime

loginout = Blueprint('loginout', __name__, static_folder='static', template_folder='templates')

##################################
#      LOGINOUT & REGISTER       #
##################################
@loginout.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect('/')

    db = Connection()
    message = ''
    if request.method == 'POST':
        log = request.form['login']
        email = request.form['email']
        password = request.form['pass']
        if log and email and password: 
            if db.register_user({'login': log, 'email': email, 'pass': password, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):
                message='Rejestracja się powiodła - teraz możesz się zalogować'
            else:
                message='Email lub login znajduje się już w bazie lub wystąpił błąd przy łączeniu z bazą'
        else:
            message='Pola nie mogą być puste'    

    return render_template('register.html', message=message)

@loginout.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect('/')

    db = Connection()
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        if email and password:
            if db.login_user({'email': email, 'pass': password}):
                message='Zostałeś zalogowany'
                session['user'] = email
            else:
                message='Błędne dane'
        else:
            message='Pola nie mogą być puste'

    return render_template('login.html', message=message)

@loginout.route('/logout')
def logout():
    db = Connection()
    session.pop('user', None)
    return redirect('/')