import os
import pandas as pd
import yfinance as yf
import datetime as dtm

TICKERS = (
    'AGG', 'EMB', 'HYG', 'IAU', 'IEMG',
    'IEFA', 'MBB', 'QQQ', 'SDY', 'SPY'
    )

HISTORY_START = '2016-01-01'

# set initial parameters
asset_prices = pd.DataFrame()
prices_path = 'static/data/asset_prices.csv'
start_date = HISTORY_START
today = dtm.date.today()

if os.path.exists(prices_path):
    asset_prices = pd.read_csv(prices_path, index_col=0)

    # if asset_prices exist, start load from last date
    last_date = dtm.datetime.strptime(
        asset_prices.last_valid_index(), '%Y-%m-%d')
    if last_date != today:
        start_date = dtm.datetime.strftime(last_date, '%Y-%m-%d')

end_date = dtm.datetime.strftime(today, '%Y-%m-%d')

yahoo_data = yf.download(
    TICKERS,
    start=start_date,
    end=end_date,
    progress=False
    )['Adj Close']

# remove corner case duplicate observations
yahoo_data = yahoo_data.groupby(yahoo_data.index).first()

# rescale prices to agree with previous close, or 100 if fresh series
if start_date == HISTORY_START:
    yahoo_data *= 100 / yahoo_data.iloc[0]
else:
    yahoo_data *= asset_prices.iloc[-1] / yahoo_data.iloc[0]

# save extended series
asset_prices = pd.concat([asset_prices, yahoo_data.iloc[1:]], axis=0)
asset_prices.index = pd.to_datetime(asset_prices.index)
asset_prices.to_csv(prices_path)

# compute performance statistics
returns = asset_prices.pct_change().dropna(how='all')
std = 16 * 100 * returns.std()
years = asset_prices.index[-1] - asset_prices.index[0]
years /= dtm.timedelta(days=365.25)
cagr = ((asset_prices.iloc[-1]/asset_prices.iloc[0]) ** (1 / years)) - 1
cagr *= 100
sr = cagr / std

statistics = pd.concat([cagr, std, sr], axis=1).transpose()
statistics = statistics.apply(lambda x: round(x, 2))
cols = statistics.columns.tolist()
statistics['METRIC'] = ['CAGR [%]', 'VOLATILITY [%]', 'SR']
statistics = statistics[['METRIC'] + [x for x in cols]]

