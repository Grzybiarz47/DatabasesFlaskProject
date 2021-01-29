from flask import session
from connection import Connection
from datetime import datetime

##################################
#            FUNCTIONS           #
##################################
def add_comment(table, id_what, id, com):
    db = Connection()
    id_user = db.call_procedure("projekt.id_użytkownika('%s')" % (session['user']))[0]['id_użytkownika']
    grade_data = db.find_user_grade(table, id_what, id, id_user)
    if com == '':
        return 'Komentarz nie może być pusty'
    else:
        db.add_comment({'id_what': id_what, 'id': grade_data[id_what + '_opinia'], 'com': com})
        return 'Dodano komentarz'

def add_grade(table, id_what, id, grade):
    db = Connection()
    id_user = db.call_procedure("projekt.id_użytkownika('%s')" % (session['user']))[0]['id_użytkownika']
    grade_data = db.find_user_grade(table, id_what, id, id_user)
    print(grade)
    if id_what + '_opinia' in grade_data:
        db.update_grade({'table': table, 'id_what': id_what, 'id': id, 'id_user': id_user, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'grade': grade})
        return 'Zmieniono ocenę'
    else:
        db.add_grade({'table': table, 'id_what': id_what, 'id': id, 'id_user': id_user, 'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'grade': grade})
        return 'Dodano ocenę'