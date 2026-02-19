import pandas as pd
import os
from data_engine import get_btc_data
from datetime import datetime
import time

SIGNAL_FILE = "signals.csv"



def check_trades():

    if not os.path.exists(SIGNAL_FILE):
        print("⚠ No signals yet. Waiting for first trade...")
        return

    df = pd.read_csv(SIGNAL_FILE)

    if df.empty:
        return


    df_1h, _ = get_btc_data()
    current_price = df_1h["close"].iloc[-1]

    updated = False

    for index, row in df.iterrows():
        if row["status"] == "OPEN":

            entry = float(row["entry"])
            stop = float(row["stop"])
            tp = float(row["tp"])
            rr = float(row["rr"])

            # Bearish logic
            if entry > tp:  # Short trade
                if current_price <= tp:
                    df.at[index, "status"] = "TP"
                    df.at[index, "result_rr"] = rr
                    df.at[index, "close_time"] = datetime.now()
                    updated = True

                elif current_price >= stop:
                    df.at[index, "status"] = "SL"
                    df.at[index, "result_rr"] = -1
                    df.at[index, "close_time"] = datetime.now()
                    updated = True

            # Bullish logic
            else:  # Long trade
                if current_price >= tp:
                    df.at[index, "status"] = "TP"
                    df.at[index, "result_rr"] = rr
                    df.at[index, "close_time"] = datetime.now()
                    updated = True

                elif current_price <= stop:
                    df.at[index, "status"] = "SL"
                    df.at[index, "result_rr"] = -1
                    df.at[index, "close_time"] = datetime.now()
                    updated = True

    if updated:
        df.to_csv(SIGNAL_FILE, index=False)
        print("✅ Trade outcomes updated")

    print(f"📊 Current BTC: {current_price}")

def run_monitor():
    while True:
        try:
            check_trades()
            time.sleep(60)
        except Exception as e:
            print("Error:", e)
            time.sleep(60)

