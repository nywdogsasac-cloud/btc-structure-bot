import pandas as pd

def detect_swings(df, lookback=3):
    df = df.copy()
    df["swing_high"] = False
    df["swing_low"] = False

    for i in range(lookback, len(df) - lookback):
        high_range = df["high"].iloc[i - lookback:i + lookback + 1]
        low_range = df["low"].iloc[i - lookback:i + lookback + 1]

        current_high = df["high"].iloc[i]
        current_low = df["low"].iloc[i]

        if current_high == high_range.max():
            df.at[df.index[i], "swing_high"] = True

        if current_low == low_range.min():
            df.at[df.index[i], "swing_low"] = True

    return df

def classify_structure(df):
    df = df.copy()
    swings = df[(df["swing_high"] == True) | (df["swing_low"] == True)]

    last_high = None
    last_low = None

    df["structure"] = None

    for idx, row in swings.iterrows():
        if row["swing_high"]:
            if last_high is not None:
                if row["high"] > last_high:
                    df.at[idx, "structure"] = "HH"
                else:
                    df.at[idx, "structure"] = "LH"
            last_high = row["high"]

        if row["swing_low"]:
            if last_low is not None:
                if row["low"] > last_low:
                    df.at[idx, "structure"] = "HL"
                else:
                    df.at[idx, "structure"] = "LL"
            last_low = row["low"]

    return df

def determine_bias(df):
    # Get last 6 structure points
    recent_structures = df[df["structure"].notna()].tail(6)

    structures = recent_structures["structure"].tolist()

    if len(structures) < 2:
        return "Neutral"

    # Bullish condition
    if "HH" in structures[-2:] and "HL" in structures[-3:]:
        return "Bullish"

    # Bearish condition
    if "LL" in structures[-2:] and "LH" in structures[-3:]:
        return "Bearish"

    return "Neutral"

def check_alignment(df, bias):
    recent = df[df["structure"].notna()].tail(3)
    structures = recent["structure"].tolist()

    if bias == "Bullish":
        if "HH" in structures or "HL" in structures:
            return True

    if bias == "Bearish":
        if "LL" in structures or "LH" in structures:
            return True

    return False
def volume_expansion(df):
    recent = df.tail(5)
    avg_volume = recent["volume"].mean()
    last_volume = recent["volume"].iloc[-1]

    if last_volume > avg_volume * 1.3:
        return True
    return False
def calculate_trade_score(bias, alignment, break_confirmed, volume_boost):
    score = 0

    if bias in ["Bullish", "Bearish"]:
        score += 2

    if alignment:
        score += 2

    if break_confirmed:
        score += 1

    if volume_boost:
        score += 1

    return score

def recent_break_structure(df):
    recent_structures = df[df["structure"].notna()].tail(2)
    structures = recent_structures["structure"].tolist()

    if len(structures) == 0:
        return False

    if structures[-1] in ["HH", "LL"]:
        return True

    return False

def detect_bullish_continuation(df):
    recent = df[df["structure"].notna()].tail(3)

    if len(recent) < 3:
        return None

    structures = recent["structure"].tolist()

    # Look for HL followed by HH
    if structures[-2] == "HL" and structures[-1] == "HH":
        entry_price = recent["high"].iloc[-1]
        stop_loss = recent["low"].iloc[-2]

        risk = entry_price - stop_loss
        take_profit = entry_price + (risk * 2)

        return {
            "entry": round(entry_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "risk_reward": 2
        }

    return None

def project_trade_levels(df_1h, bias):

    if "structure" not in df_1h.columns:
        return None, None, None, None

    swings = df_1h[df_1h["structure"].isin(["HH", "LH", "HL", "LL"])]

    if len(swings) < 2:
        return None, None, None, None

    last_high = swings[swings["structure"].isin(["HH", "LH"])].tail(1)
    last_low = swings[swings["structure"].isin(["HL", "LL"])].tail(1)

    if last_high.empty or last_low.empty:
        return None, None, None, None

    high_price = last_high["high"].iloc[-1]
    low_price = last_low["low"].iloc[-1]

    if bias == "Bearish":
        entry = low_price
        stop_loss = high_price
        risk = stop_loss - entry
        take_profit = entry - (risk * 2)

    elif bias == "Bullish":
        entry = high_price
        stop_loss = low_price
        risk = entry - stop_loss
        take_profit = entry + (risk * 2)

    else:
        return None, None, None, None

    rr = round(abs((take_profit - entry) / (entry - stop_loss)), 2)

    return entry, stop_loss, take_profit, rr


