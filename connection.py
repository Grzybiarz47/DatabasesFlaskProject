import psycopg2
import psycopg2.extras
import urllib.parse as up
import os
from psycopg2 import Error

##################################
#      DATABASE CONNECTION       #
##################################

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

class DatabaseConnection:

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

    def close(self):
        if (self.connection):
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection closed")

###################################