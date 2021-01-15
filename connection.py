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

    def make_dict(self, result):
        ans = []
        for row in result:
            ans.append(dict(row))
        return ans

    def close(self):
        return self.__del__()

    def __del__(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection closed")

##################################

    def find_movie_series_game(self, query):
        full_query_series = """
        SELECT id_serial, nazwa
        FROM "projekt"."SERIAL" as serial 
        WHERE serial.nazwa LIKE '%s'
        ORDER BY nazwa
        """
        full_query_film = """
        SELECT id_film, nazwa
        FROM "projekt"."FILM" as film        
        WHERE film.nazwa LIKE '%s' 
        ORDER BY nazwa
        """
        full_query_game = """
        SELECT id_gra, nazwa
        FROM "projekt"."GRA" as gra       
        WHERE gra.nazwa LIKE '%s' 
        ORDER BY nazwa
        """
        result = []

        self.cursor.execute(full_query_series % (query))
        result.append(self.make_dict(self.cursor.fetchall()))
        self.cursor.execute(full_query_film % (query))
        result.append(self.make_dict(self.cursor.fetchall()))
        self.cursor.execute(full_query_game % (query))
        result.append(self.make_dict(self.cursor.fetchall()))

        print(full_query_series % (query))
        print(full_query_film % (query))
        print(full_query_game % (query))
        return result

    def find_info(self, table, id_what, id):
        full_query = """
        SELECT * 
        FROM "projekt"."%s"
        WHERE %s = %s
        """

        self.cursor.execute(full_query % (table, id_what, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (table, id_what, id))
        return result

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
    
    def find_seasons(self, id):
        full_query = """
        SELECT * 
        FROM "projekt"."SEZON" 
        WHERE id_serial = %s
        """
        
        self.cursor.execute(full_query % (id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id))
        return result
    
    def find_season_info(self, id_serial, id_sezon):
        full_query = """
        SELECT nazwa, sezon.rok_produkcji
        FROM "projekt"."SEZON" as sezon JOIN "projekt"."SERIAL" USING(id_serial) 
        WHERE id_serial = %s and id_sezon = %s
        """

        self.cursor.execute(full_query % (id_serial, id_sezon))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id_serial, id_sezon))
        return result

    def find_chapters(self, id):
        full_query = """
        SELECT nazwa 
        FROM "projekt"."ODCINEK" 
        WHERE id_sezon = %s
        """

        self.cursor.execute(full_query % (id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id))
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
    
    def find_artist_type(self, id):
        full_query = """
        SELECT typ
        FROM "projekt"."RODZAJ_ARTYSTY"
        WHERE id_artysta = %s
        """
        
        self.cursor.execute(full_query % (id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id))
        return result
    
    def find_roles(self, id):
        full_query = """
        (SELECT nazwa, postac, rok_produkcji
        FROM "projekt"."ARTYSTA" JOIN "projekt"."ARTYSTA_FILM" USING(id_artysta)
                                 JOIN "projekt"."FILM" as film USING(id_film)
        WHERE id_artysta = %s
        UNION
        SELECT nazwa, postac, rok_produkcji
        FROM "projekt"."ARTYSTA" JOIN "projekt"."ARTYSTA_SERIAL" USING(id_artysta)
                                 JOIN "projekt"."SERIAL" as serial USING(id_serial)
        WHERE id_artysta = %s)
        ORDER BY rok_produkcji
        """

        self.cursor.execute(full_query % (id, id))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (id, id))
        return result
    
    def find_account(self, user):
        full_query = """
        SELECT login, email, data_dolaczenia
        FROM "projekt"."UZYTKOWNIK"
        WHERE email = '%s'
        """

        self.cursor.execute(full_query % (user))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (user))
        return result
    
    def find_users(self, name, user):
        full_query = """
        SELECT id_user, login
        FROM "projekt"."UZYTKOWNIK"
        WHERE email != '%s' and login LIKE '%s'
        """

        self.cursor.execute(full_query % (user, name))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (user, name))
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
    
    def find_observed(self, email):
        full_query = """
        SELECT * FROM "projekt"."observed%s" 
        """

        self.cursor.execute(full_query % (email))
        result = self.make_dict(self.cursor.fetchall())

        print(full_query % (email))
        return result

##################################

    def valid_email_login(self, email, login):
        full_query = """
        SELECT COUNT(*)
        FROM "projekt"."UZYTKOWNIK"
        WHERE email = '%s' or login = '%s'
        """

        self.cursor.execute(full_query % (email, login))
        result = self.make_dict(self.cursor.fetchall())

        if result[0]['count'] != 0:
            result = False
        else:
            result = True

        print(full_query % (email, login))
        return result

    def register_user(self, data):
        full_query = """
        INSERT INTO "projekt"."UZYTKOWNIK" VALUES
        ((SELECT projekt.next_id('UZYTKOWNIK', 'id_user')), '%s', '%s', '%s', '%s') 
        """

        try:
            self.cursor.execute(full_query % (data['email'], data['date'], data['pass'], data['login']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding new record to database", error)
            return False

        print(full_query % (data['email'], data['date'], data['pass'], data['login']))
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

    def add(self, data):
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
        self.create_observed_view(data['user'])
    
    def delete(self, data):
        full_query = """
        DELETE FROM "projekt"."OBSERWOWANY" WHERE id_obserwowany = %s and id_user = %s
        """

        try:
            self.cursor.execute(full_query % (data['id'], data['id_user']))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while adding new record to database", error)

        print(full_query % (data['id'], data['id_user']))
        self.create_observed_view(data['user'])


    def create_observed_view(self, user):
        full_query = """
        CREATE OR REPLACE VIEW "projekt"."observed%s" AS
        SELECT id_user, login
        FROM "projekt"."UZYTKOWNIK" JOIN (
        SELECT id_obserwowany 
        FROM "projekt"."UZYTKOWNIK" JOIN "projekt"."OBSERWOWANY" USING(id_user)
        WHERE email = '%s') as p 
        ON p.id_obserwowany = id_user
        """

        try:
            self.cursor.execute(full_query % (user, user))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while creating view", error)

        print(full_query % (user, user))
    
    def drop_observed_view(self, user):
        full_query = """
        DROP VIEW IF EXISTS "projekt"."observed%s"
        """

        try:
            self.cursor.execute(full_query % (user))
            self.connection.commit()
        
        except (Exception, Error) as error:
            print("Error while creating view", error)

        print(full_query % (user))
    




