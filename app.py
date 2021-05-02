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


@app.route('/portfolios/<username>', methods=['GET', 'POST'])
def portfolios(username):
    # portfolio = get_portfolio_from_email(email)
    portfolio = pd.DataFrame({'A': [1, 2, 3], 'B': [3, 4, 5]})
    template = render_template(
        'portfolios.html',
        username=username,
        column_names=portfolio.columns.tolist(),
        row_data=list(portfolio.values.tolist())
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
        session['user'] = registration['email']
        flash('Registered Successfully!')
        username = get_username_from_email(session['user'])
        return redirect(url_for('portfolios'), username)

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
                session['user'] = existing_user['email']
                username = get_username_from_email(session['user'])
                flash(f'Welcome {username}')
                return redirect(url_for('portfolios', username=username))
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

    # for ptf in mongo.db.portfolios.find():
    #     for k, v in ptf.items():
    #         if k != '_id':
    #             for u, w in v.items():
    #                 print(u, w)
    # mongo.db.portfolios.insert_one(df.transpose().to_dict())

    # portfolios = mongo.db.portfolios.find()
    # for ptf in portfolios:
    #     print(record_to_dataframe(ptf))
    # print(PRICES)
