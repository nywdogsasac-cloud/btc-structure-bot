from binance.client import Client
import pandas as pd
import os

# Public API (no key needed for candles)
client = Client()

def get_klines(symbol="BTCUSDT", interval="1h", limit=200):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    df = pd.DataFrame(klines, columns=[
        "open_time","open","high","low","close","volume",
        "close_time","qav","num_trades",
        "taker_base_vol","taker_quote_vol","ignore"
    ])

    df = df[["open_time","open","high","low","close","volume"]]
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    
    for col in ["open","high","low","close","volume"]:
        df[col] = df[col].astype(float)

    return df

def get_btc_data():
    df_1h = get_klines(interval="1h")
    df_4h = get_klines(interval="4h")
    return df_1h, df_4h

try:
    import pandas as pd
    from binance.client import Client
    print("pandas and binance imported successfully")
except ImportError as e:
    import sys
    print("Import error:", e)
    print("Using Python:", sys.executable)
    raise