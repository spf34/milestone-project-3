import os
import pandas as pd
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for
    )
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists('env.py'):
    import env

import asset_data
PRICES = asset_data.asset_prices
TICKERS = asset_data.TICKERS

app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

USER_FIELDS = ('first', 'last', 'email')


@app.route('/')
def get_users():
    users = mongo.db.users.find()
    return render_template('users.html', users=users)


@app.route('/portfolio/<username>', methods=['GET', 'POST'])
def portfolio(username):
    # portfolio = get_portfolio_from_email(email)
    portfolio = pd.DataFrame({
        'A': [x for x in range(20)],
        'E': [3 * x for x in range(20)]
        })

    template = render_template(
        'portfolio.html',
        username=username,
        columns=portfolio.columns.tolist(),
        rows=list(portfolio.values.tolist()),
        zip=zip
        )
    return template


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # check to see whether the email address is already registered
        existing_user = mongo.db.users.find_one({
            'email': request.form.get('email').lower()
            })

        if existing_user:
            flash('User already exists')
            return redirect(url_for('register'))

        # check that password agrees with repeat-password
        password = request.form.get('password')
        if password != request.form.get('repeat-password'):
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # generate user record and add to db
        user_details = {
            field: request.form.get(field).lower() for field in USER_FIELDS
            }
        password = {
            'password': generate_password_hash(password)
            }
        registration = {**user_details, **password}
        mongo.db.users.insert_one(registration)

        # put the new user into session cookie
        username = get_username_from_email(registration['email'])
        session['username'] = username
        flash('Registered Successfully!')

        return redirect(url_for('portfolio'), username)

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        existing_user = mongo.db.users.find_one({
            'email': request.form.get('email').lower()
            })
        if existing_user:
            password = request.form.get('password')
            if check_password_hash(existing_user['password'], password):
                username = get_username_from_email(existing_user['email'])
                session['username'] = username
                flash(f'Welcome {username}')

                return redirect(url_for('portfolio', username=username))
            else:
                flash('Email or password not recognised')
                return redirect(url_for('login'))
        else:
            flash('Email or password not recognised')
            return redirect(url_for('login'))
    return render_template('login.html')


def record_to_dataframe(data):
    return pd.DataFrame(data).drop('_id', axis=1).transpose()


def get_username_from_email(email):
    user_info = mongo.db.users.find_one({'email': email})
    first = user_info['first']
    last = user_info['last']
    return first.capitalize() + last.capitalize()


def get_portfolio_from_email(email):
    user_info = mongo.db.users.find({'email': email})
    user_id = user_info['_id']
    mongo.db.portfolios.find({'user_id': user_id})
    # ToDo: implement rest of this method
    return

if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True
    )

    # print(PRICES)
