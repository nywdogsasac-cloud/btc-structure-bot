import time
from data_engine import get_btc_data
from structure_engine import (
    detect_swings,
    classify_structure,
    determine_bias,
    check_alignment,
    volume_expansion,
    recent_break_structure,
    calculate_trade_score,
)
import requests

TELEGRAM_TOKEN = "8349820438:AAGv826Hu7WmT4ex908DEu1-Ladx_jnj8TY"
CHAT_ID = "5220750983"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

alert_active = False

while True:
    try:
        df_1h, df_4h = get_btc_data()

        df_1h = detect_swings(df_1h)
        df_4h = detect_swings(df_4h)

        df_1h = classify_structure(df_1h)
        df_4h = classify_structure(df_4h)

        bias = determine_bias(df_4h)
        alignment = check_alignment(df_1h, bias)
        break_confirmed = recent_break_structure(df_1h)
        volume_boost = volume_expansion(df_1h)

        score = calculate_trade_score(
            bias,
            alignment,
            break_confirmed,
            volume_boost
        )

        print(f"Bias: {bias} | Score: {score}")

        if score >= 3 and not alert_active:
            message = f"""
🚨 BTC TRADE SIGNAL 🚨

4H Bias: {bias}
1H Alignment: {alignment}
Trade Score: {score}/6

Check dashboard for entry.
"""
            send_telegram_alert(message)
            alert_active = True

        if score < 3:
            alert_active = False

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
