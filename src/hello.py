from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import json

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

app.config['SECRET_KEY'] = '12345'

# initialize the app with the extension
db.init_app(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/logged')
def logged():
    return render_template('logged.html', name=request.args['name'])


@app.route('/login', methods=('GET', 'POST'))
def login():
    with get_db_connection() as conn:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            # print(email)
            # print(password)
            if not email or not password:
                flash('Введите логин и пароль!')
            else:
                find_user = conn.execute('SELECT * FROM users WHERE email=? AND password=?',
                            (email,password,)
                            ).fetchone()
                if find_user:
                    return redirect(url_for('logged', name=find_user['name']))
                else:
                    flash('Неверный логин или пароль!')
    return redirect(url_for('index'))
    