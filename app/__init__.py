from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
import sqlite3
import os
from sqlite3 import Error

# create and configure app
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)

# TODO: Handle login management better, maybe with flask_login?



# get an instance of the db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db

# initialize db for the first time
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# perform generic query, not very secure yet
def query_db(query, one=False):
    db = get_db()
    cursor = db.execute(query)
    rv = cursor.fetchall()
    cursor.close()
    db.commit()
    return (rv[0] if rv else None) if one else rv

# TODO: Add more specific queries to simplify code




def query_userId(db, userId):
    sql =  'SELECT * FROM Users WHERE id= ?'
    try: 
        cur = db.cursor()
        cur.execute(sql, (userId,))
        db.commit()
        user = cur.fetchall()
    except Error as e:
        print(e)
    return user

def query_username(db, username):
    sql =  'SELECT * FROM Users WHERE username= ?'
    try: 
        cur = db.cursor()
        cur.execute(sql, (username,))
        db.commit()
        user = cur.fetchall()
    except Error as e:
        print(e)
    return user

def query_formRegister(db, username, first_name, last_name, password):
    sql =  'INSERT INTO Users (username, first_name, last_name, password) VALUES(?, ?, ?, ?)'
    try: 
        cur = db.cursor()
        cur.execute(sql, (username, first_name, last_name, password,))
        db.commit()
    except Error as e:
        print(e)

def query_postStream(db, u_id, content, image, creation_time):
    sql =  'INSERT INTO Posts (u_id, content, image, creation_time) VALUES(?, ?, ?, ?)'
    try: 
        print(u_id, content, image, creation_time, "verdier")
        cur = db.cursor()
        cur.execute(sql, (u_id, content, image, creation_time,))
        db.commit()
    except Error as e:
        print(e)


# automatically called when application is closed, and closes db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# initialize db if it does not exist
if not os.path.exists(app.config['DATABASE']):
    init_db()

if not os.path.exists(app.config['UPLOAD_PATH']):
    os.mkdir(app.config['UPLOAD_PATH'])

from app import routes