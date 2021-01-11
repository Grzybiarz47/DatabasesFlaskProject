import psycopg2
import urllib.parse as up
import os
from psycopg2 import Error
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
else:
    app.debug = False

##################################
#      DATABASE CONNECTION       #
##################################

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ["DATABASE_URL"])

class DatabaseOperation:

    def test(self):
        try:
            connection = psycopg2.connect(database=url.path[1:],
                                    user=url.username,
                                    password=url.password,
                                    host=url.hostname,
                                    port=url.port)

            cursor = connection.cursor()
            print("PostgreSQL server information")
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")

            query = """ SELECT * FROM "projekt"."UZYTKOWNIK" """
            cursor.execute(query)
            record = cursor.fetchall()
            print("Result ", record)

        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)

        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

###################################

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    db = DatabaseOperation()
    db.test()
    app.run()

