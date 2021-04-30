import seaborn as sns
import yfinance as yf
import datetime as dtm
import matplotlib.pyplot as plt

sns.set(rc={'figure.figsize': (18, 6)})

TICKERS = (
    'AGG', 'EMB', 'HYG', 'IAU', 'IEMG', 'IEFA', 'MBB',
    'QQQ', 'SDY', 'SPY', 'TIP', 'VTV', 'VUG', 'XLC',
    'XLE', 'XLF', 'XLI', 'XLK', 'XLV', 'XLY'
    )

today = dtm.date.today()
end = dtm.datetime.strftime(today, '%Y-%m-%d')
data = yf.download(
    TICKERS,
    start='2016-01-01',
    end=end,
    progress=False
    )['Adj Close']

data *= 100 / data.iloc[0]
