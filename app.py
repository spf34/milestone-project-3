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
HISTORY_START = pd.to_datetime(asset_data.HISTORY_START, format='%Y-%m-%d')

# app setup
app = Flask(__name__)

app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET_KEY')

mongo = PyMongo(app)

USER_FIELDS = ('first', 'last', 'email')

# helper methods


def set_session_info(email):
    session['email'] = email
    session['username'] = get_username_from_email(email)


def record_to_dataframe(data):
    return pd.DataFrame(data).drop('_id', axis=1).transpose()


def get_username_from_email(email):
    user_info = mongo.db.users.find_one({'email': email})
    first = user_info['first']
    last = user_info['last']
    return first.capitalize() + last.capitalize()


def get_portfolio_from_username(username):
    return mongo.db.portfolios.find_one({'username': username})


def edit_records():
    pass


def upload_records(records, username, overwrite=True):
    # username = session['username']
    data = records.transpose().to_dict()

    # remove dates already present in db if overwrite is set to false
    if not overwrite:
        current_portfolio = get_portfolio_from_username(username)
        for field in current_portfolio:
            if field not in ['_id', 'username']:
                data[field] = current_portfolio[field]

    records_to_upload = {
        **{'username': username},
        **data
        }
    mongo.db.portfolios.insert_one(records_to_upload)


def validate_portfolio_records(records):
    # check valid assets passed
    columns = records.columns.tolist()
    assert all([x.upper() in TICKERS for x in columns])

    # convert index to datetimes
    try:
        records.index = pd.to_datetime(records.index, format='%Y-%m-%d')
    except ValueError:
        flash('Unable to parse dates. Please use the format: "yyyy/mm/dd"')

    # check for valid dates
    assert records.first_valid_index() >= HISTORY_START

    return records, True

# routing methods


@app.route('/')
def get_users():
    users = mongo.db.users.find()
    return render_template('users.html', users=users)


@app.route('/portfolio_overview/<username>')
def portfolio_overview(username):
    if not session.get('username'):
        return redirect(url_for('login'))

    # portfolio = get_portfolio_from_email(email)
    portfolio = pd.DataFrame({
        'A': [x for x in range(20)],
        'E': [3 * x for x in range(20)]
        })

    return render_template(
        'portfolio_overview.html',
        username=username,
        columns=portfolio.columns.tolist(),
        rows=list(portfolio.values.tolist()),
        zip=zip
        )


@app.route('/portfolio_construction/<username>', methods=['GET', 'POST'])
def portfolio_construction(username):
    if request.method == 'POST':
        filepath = request.files.get('file')
        records = pd.read_csv(filepath, index_col=0)
        records, validated = validate_portfolio_records(records)

        if not validated:
            flash('Unable to process records file')
            return render_template('portfolio_construction.html')

        upload_records(records, session['email'])

        flash('Records successfully processed')
        assets = records.loc[:, records.max() > 0].columns.tolist()
        return render_template(
            'portfolio_construction.html',
            number_records=len(records),
            assets=assets
            )

    return render_template('portfolio_construction.html')


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
        set_session_info(registration['email'])
        flash('Registered Successfully!')
        return redirect(
            url_for('portfolio_overview'), username=session['username']
            )

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
                set_session_info(existing_user['email'])
                username = session['username']

                flash(f'Welcome {username}')
                return redirect(
                    url_for('portfolio_overview', username=username)
                    )
            else:
                flash('Email or password not recognised')
                return redirect(url_for('login'))
        else:
            flash('Email or password not recognised')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    flash('You have been logged out')
    session.pop('username')
    return redirect(url_for('login'))


if __name__ == '__main__':
    # app.run(
    #     host=os.environ.get('IP'),
    #     port=int(os.environ.get('PORT')),
    #     debug=True
    # )

    # records1 = pd.read_csv('static/data/records1.csv', index_col=0)
    # print(records1)
    email = 'samuel.p.forster@gmail.com'
    username = get_username_from_email(email)
    # upload_records(records1, username, overwrite=True)

    records2 = pd.read_csv('static/data/records2.csv', index_col=0)
    print(records2)

    print('CURRENT PORTFOLIO')
    current_portfolio = get_portfolio_from_username(username)
    for k, v in current_portfolio.items():
        print(f'{k}: {v}')

    upload_records(records2, username, overwrite=False)
    
    print('CURRENT PORTFOLIO')
    current_portfolio = get_portfolio_from_username(username)
    for k, v in current_portfolio.items():
        print(f'{k}: {v}')
