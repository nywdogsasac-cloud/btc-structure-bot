import csv
import os
from datetime import datetime

SIGNAL_FILE = "signals.csv"
TRADE_FILE = "trades.csv"


def initialize_file(file, headers):
    if not os.path.exists(file):
        with open(file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def log_signal(data):
    headers = [
        "timestamp",
        "bias",
        "score",
        "entry",
        "stop",
        "tp",
        "rr",
        "market_price",
        "timeframe",
        "status",
        "result_rr",
        "close_time"
    ]

    initialize_file(SIGNAL_FILE, headers)

    with open(SIGNAL_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)



def log_trade(data):
    headers = [
        "timestamp",
        "entry",
        "stop",
        "tp",
        "result",
        "rr_achieved",
        "notes"
    ]

    initialize_file(TRADE_FILE, headers)

    with open(TRADE_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
