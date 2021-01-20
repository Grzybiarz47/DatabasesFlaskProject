import psycopg2
import psycopg2.extras
import urllib.parse as up
import os
from psycopg2 import Error
from datetime import datetime

##################################
#      DATABASE CONNECTION       #
##################################

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

class Connection:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(database=url.path[1:],
                                    user=url.username,
                                    password=url.password,
                                    host=url.hostname,
                                    port=url.port)

            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def __del__(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection closed")

    def make_dict(self, result):
        ans = []
        for row in result:
            ans.append(dict(row))
        return ans

##################################

    def call_procedure(self, proc):
        prefix = "SELECT * FROM "
        self.cursor.execute(prefix + proc)
        result = self.make_dict(self.cursor.fetchall())

        print(proc)
        return result

##################################

    def find_info(self, table, id_what, id):
        full_query = """
        SELECT *
        FROM "projekt"."%s"
        WHERE %s = %s
        """

        self.cursor.execute(full_query % (table, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (table, id_what, id))
        return result[0]

    def find_grade(self, table, id_what, id):
        full_query = """
        SELECT CAST(AVG(ocena) AS DECIMAL(7,4))as ocena
        FROM "projekt"."UZYTKOWNIK_%s"
        WHERE %s = %s
        """

        self.cursor.execute(full_query % (table, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        if result[0]['ocena'] == None:
            result[0]['ocena'] = 'Brak ocen'

        print(full_query % (table, id_what, id))
        return result[0]
    
    def find_user_grade(self, table, id_what, id, id_user):
        full_query = """
        SELECT %s_opinia, ocena
        FROM "projekt"."UZYTKOWNIK_%s" JOIN "projekt"."UZYTKOWNIK" USING(id_user)
        WHERE id_user = %s and %s = %s
        """

        self.cursor.execute(full_query % (id_what, table, id_user, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id_what, table, id_user, id_what, id))
        if result == []:
            result = [{'ocena': 'Brak oceny'}]
        return result[0]

    def find_cast(self, table, id_what, id):
        full_query = """
        SELECT id_artysta, imie, nazwisko, rola, postac
        FROM "projekt"."%s" JOIN "projekt"."ARTYSTA_%s" USING (%s)
                            JOIN "projekt"."ARTYSTA" USING(id_artysta)
        WHERE %s = %s
        ORDER BY rola
        """

        self.cursor.execute(full_query % (table, table, id_what, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (table, table, id_what, id_what, id))
        return result
    
    def find_prizes(self, id_what, id):
        full_query = """
        SELECT nazwa, rok_przyznania
        FROM "projekt"."NAGRODA"
        WHERE %s = %s 
        """

        self.cursor.execute(full_query % (id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id_what, id))
        return result

    def find_id_user(self, email):
        full_query = """
        SELECT id_user 
        FROM "projekt"."UZYTKOWNIK" 
        WHERE email = '%s'
        """

        self.cursor.execute(full_query % (email))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (email))
        return result[0]['id_user']
    
    def find_comments(self, table, email, id_what, id):
        full_query = """
        SELECT id_komentarz, recenzja, login
        FROM "projekt"."UZYTKOWNIK_%s" JOIN "projekt"."KOMENTARZ" USING(%s_opinia)
                                       JOIN (SELECT * FROM projekt.wyszukaj_obserwowanych('%s')) as o USING(id_user)
        WHERE %s = %s
        ORDER BY id_komentarz DESC
        """

        self.cursor.execute(full_query % (table, id_what, email, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (table, id_what, email, id_what, id))
        return result

##################################

    def register_user(self, data):
        full_query = """
        INSERT INTO "projekt"."UZYTKOWNIK" VALUES
        ((SELECT projekt.next_id('UZYTKOWNIK', 'id_user')), '%s', '%s', '%s', '%s') 
        """
        check_query = """
        SELECT COUNT(*) FROM "projekt"."UZYTKOWNIK" 
        """

        try:
            self.cursor.execute(check_query)
            result1 = self.make_dict(self.cursor.fetchall())
            print(check_query)

            self.cursor.execute(full_query % (data['email'], data['date'], data['pass'], data['login']))
            self.connection.commit()
            print(full_query % (data['email'], data['date'], data['pass'], data['login']))

            self.cursor.execute(check_query)
            result2 = self.make_dict(self.cursor.fetchall())
            print(check_query)

            if result1[0]['count'] == result2[0]['count']:
                return False

        except (Exception, Error) as error:
            print("Error while adding new record to database", error)
            return False

        return True

    def login_user(self, data):
        full_query = """
        SELECT COUNT(*)
        FROM "projekt"."UZYTKOWNIK"
        WHERE email = '%s' and haslo = '%s'
        """

        self.cursor.execute(full_query % (data['email'], data['pass']))
        result = self.make_dict(self.cursor.fetchall())

        if result[0]['count'] != 0:
            result = True
        else:
            result = False

        print(full_query % (data['email'], data['pass']))
        return result
    
##################################

    def add_to_observed(self, data):
        full_query = """
        INSERT INTO "projekt"."OBSERWOWANY" VALUES
        ((SELECT id_user FROM "projekt"."UZYTKOWNIK" WHERE email = '%s'), %s, '%s')
        """

        try:
            self.cursor.execute(full_query % (data['user'], data['id'], data['date']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding new record to database", error)

        print(full_query % (data['user'], data['id'], data['date']))
    
    def add_grade(self, data):
        full_query = """
        INSERT INTO "projekt"."UZYTKOWNIK_%s" VALUES
        (projekt.next_id('UZYTKOWNIK_%s', '%s_opinia'), %s, %s, %s, '%s')
        """

        try:
            self.cursor.execute(full_query % (data['table'], data['table'], data['id_what'], data['id_user'], data['id'], data['grade'], data['date']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding new record to database", error)

        print(full_query % (data['table'], data['table'], data['id_what'], data['id_user'], data['id'], data['grade'], data['date']))

    def add_comment(self, data):
        full_query = """
        INSERT INTO "projekt"."KOMENTARZ" (id_komentarz, %s_opinia, recenzja) VALUES
        (projekt.next_id('KOMENTARZ', 'id_komentarz'), %s, '%s')
        """

        try:
            self.cursor.execute(full_query % (data['id_what'], data['id'], data['com']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding record in database", error)

        print(full_query % (data['id_what'], data['id'], data['com']))

##################################

    def update_grade(self, data):
        full_query = """
        UPDATE "projekt"."UZYTKOWNIK_%s" 
        SET ocena = %s, data_oceny = '%s'
        WHERE id_user = %s and %s = %s 
        """

        try:
            self.cursor.execute(full_query % (data['table'], data['grade'], data['date'], data['id_user'], data['id_what'], data['id']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while updating record in database", error)

        print(full_query % (data['table'], data['grade'], data['date'], data['id_user'], data['id_what'], data['id']))

##################################

    def delete_from_observed(self, data):
        full_query = """
        DELETE FROM "projekt"."OBSERWOWANY" WHERE id_obserwowany = %s and id_user = %s
        """

        try:
            self.cursor.execute(full_query % (data['id'], data['id_user']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding new record to database", error)

        print(full_query % (data['id'], data['id_user']))
    




