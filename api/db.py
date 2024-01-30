import api
import psycopg2
from flask import g

def get_db(app=None):
    if ('db' not in g) and app is not None:
        g.db = psycopg2.connect(**{
        "database": app.config["DBNAME"],
        "user": app.config["DBUSER"],
        "password": app.config["DBPWD"],
        "host": app.config["DBHOST"],
        "port": app.config["DBPORT"]
        })

    return g.db

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_item(id):
    db = get_db()
    curs = db.cursor()

    curs.execute("")


def edit_item(id, form):
    return True