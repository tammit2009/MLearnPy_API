from binance import Client
import os
import pandas as pd
import pytz

# from src.config import binance_keys
# client = Client(binance_keys.api_key, binance_keys.secret_key)
client = Client(os.environ.get("BINANCE_API_KEY"), os.environ.get("BINANCE_SECRET_KEY"))

my_tz = pytz.timezone('Africa/Lagos')

def get_minute_data(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + ' min ago UTC + 1'))
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame = frame.astype(float)
    return frame

