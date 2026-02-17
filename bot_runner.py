import time
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

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

# =========================
# ENV VARIABLES (RENDER SAFE)
# =========================
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    raise ValueError("❌ BOT_TOKEN or CHAT_ID not set in environment variables.")

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram_alert(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("✅ Telegram alert sent.")
    except Exception as e:
        print("❌ Telegram Error:", e)

# =========================
# STARTUP MESSAGE
# =========================
send_telegram_alert("🚀 BTC Structure Bot is now running 24/7")

alert_active = False

# =========================
# MAIN LOOP
# =========================
while True:
    try:
        print(f"\n⏳ Running check at {datetime.now()}")

        # Get data
        df_1h, df_4h = get_btc_data()

        # Apply structure logic
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

        print(f"📊 Bias: {bias} | Score: {score}")

        # =========================
        # ALERT LOGIC (Score >= 3)
        # =========================
        if score >= 3 and not alert_active:

            message = f"""
🚨 *BTC TRADE SIGNAL* 🚨

📈 4H Bias: *{bias}*
🔄 1H Alignment: *{alignment}*
🔥 Trade Score: *{score}/6*

Check dashboard for possible entry.
Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

            send_telegram_alert(message)
            alert_active = True

        # Reset alert if conditions weaken
        if score < 3:
            alert_active = False

        # Run every 1 minute
        time.sleep(60)

    except Exception as e:
        print("❌ System Error:", e)
        time.sleep(60)
