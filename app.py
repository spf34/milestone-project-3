import os
import pandas as pd
import datetime as dtm
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

# constants
PRICES = asset_data.asset_prices
TICKERS = asset_data.TICKERS
ZERO_RECORD = {ticker: 0.0 for ticker in TICKERS}
STATISTICS = asset_data.statistics
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


def get_username_from_email(email):
    user_info = mongo.db.users.find_one({'email': email})
    first = user_info['first']
    last = user_info['last']
    return first.capitalize() + last.capitalize()


def get_portfolio_from_username(username):
    return mongo.db.portfolios.find_one({'username': username})


def dataframe_to_records(df, username):
    data = df.transpose().to_dict()
    records = []

    for date in data:
        r = {**{'username': username}, **{'date': date}, **data[date]}
        records.append(r)
    return records


def get_portfolio_from_username2(username):
    """Returns dataframe of all positions in db for given username"""
    positions = mongo.db.portfolios.find({'username': username})
    df = pd.DataFrame()
    for p in positions:
        df = pd.concat(
            [df, pd.DataFrame(p.values(), index=p.keys())], axis=1)
    df = df.transpose().drop(['_id', 'username'], axis=1)
    return df.set_index('date').sort_index()


def upload_records(records, username, overwrite=True):
    for ticker in TICKERS:
        if ticker not in records:
            records[ticker] = 0

    if not mongo.db.portfolios.find_one({'username': username}):
        print('NOT FOUND')
        records_to_upload = dataframe_to_records(records, username)
        mongo.db.portfolios.insert_many(records_to_upload)
        return

    current_portfolio = get_portfolio_from_username2(username)
    for date in current_portfolio.index:
        if not overwrite:
            # use current portfolio if we do not want to overwrite
            records.loc[date] = current_portfolio.loc[date]
        elif (overwrite and date not in records.index):
            mongo.db.portfolios.delete_one(
                {'username': username, 'date': date})

    records_to_update = dataframe_to_records(
        records.loc[records.index.isin(current_portfolio.index)],
        username)

    for r in records_to_update:
        mongo.db.portfolios.update_one(
            {'username': username, 'date': r['date']},
            {'$set': r})

    records_to_upload = dataframe_to_records(
        records.loc[~records.index.isin(current_portfolio.index)],
        username)
    if(records_to_upload):
        mongo.db.portfolios.insert_many(records_to_upload)

    flash('Successful Record upload')


def validate_portfolio_records(records):
    # check valid assets passed
    columns = records.columns.tolist()
    assert all([x.upper() in TICKERS for x in columns])

    # check no repeated columns
    assert max([columns.count(x) for x in TICKERS]) == 1

    # convert index to str
    try:
        records.index = pd.to_datetime(records.index, format='%Y-%m-%d')
    except TypeError:
        flash('Unable to parse dates. May already be of type str')

    # check for valid dates
    assert records.first_valid_index() >= HISTORY_START

    records.index = [
        dtm.datetime.strftime(d, '%Y-%m-%d')
        for d in records.index
        ]

    return records, True

# routing methods


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/assets')
def assets():

    return render_template(
        'assets.html',
        columns=STATISTICS.columns.tolist(),
        rows=STATISTICS.values.tolist(),
        zip=zip
        )


@app.route('/portfolio_overview/<username>')
def portfolio_overview(username):
    if not session.get('username'):
        return redirect(url_for('login'))

    portfolio = pd.DataFrame(
        get_portfolio_from_username2(username)).reset_index('date')
    portfolio.rename(columns={'date': 'DATE'}, inplace=True)

    return render_template(
        'portfolio_overview.html',
        username=username,
        columns=portfolio.columns.tolist(),
        rows=portfolio.values.tolist(),
        zip=zip
        )


@app.route('/portfolio_position_upload/<username>', methods=['GET', 'POST'])
def portfolio_position_upload(username):
    if request.method == 'POST':
        # get data from request
        overwrite = 'overwrite' in request.form
        date = request.form['position_date']
        date = dtm.datetime.strftime(pd.to_datetime(date), format='%Y-%m-%d')
        weight = request.form['position_weight']
        ticker = request.form['ticker']

        records = pd.DataFrame({ticker: [weight]}, index=[date])
        upload_records(records, session['username'], overwrite=overwrite)

    return render_template('portfolio_position_upload.html')


@app.route('/portfolio_bulk_upload/<username>', methods=['GET', 'POST'])
def portfolio_bulk_upload(username):
    if request.method == 'POST':
        # get data from request
        overwrite = 'overwrite' in request.form
        filepath = request.files.get('file')
        records = pd.read_csv(filepath, index_col=0)

        # validate and upload record input
        records, validated = validate_portfolio_records(records)
        if not validated:
            flash('Unable to process records file')
            return render_template('portfolio_bulk_upload.html')
        upload_records(records, session['username'], overwrite=overwrite)

    return render_template('portfolio_bulk_upload.html')


@app.route('/logout')
def logout():
    flash('You have been logged out')
    session.pop('username')
    return redirect(url_for('login'))


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
            url_for('portfolio_overview', username=session['username'])
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


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True
    )

    # print(STATISTICS)

    # email = 'samuel.p.forster@gmail.com'
    # username = get_username_from_email(email)
    # overwrite = True

    # records = pd.read_csv('static/data/records2.csv', index_col=0)
    # upload_records(records, username, overwrite=False)

    # current_portfolio = get_portfolio_from_username2(username)
    # print('CURRENT PORTFOLIO')
    # print(current_portfolio)
