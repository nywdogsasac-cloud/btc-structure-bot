import streamlit as st
import requests

from data_engine import get_btc_data
from streamlit_autorefresh import st_autorefresh

TELEGRAM_TOKEN = "8349820438:AAGv826Hu7WmT4ex908DEu1-Ladx_jnj8TY"
CHAT_ID = "5220750983"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

from structure_engine import (
    detect_swings,
    classify_structure,
    determine_bias,
    check_alignment,
    volume_expansion,
    recent_break_structure,
    calculate_trade_score,
    detect_bullish_continuation
)

st.set_page_config(layout="wide")
# Auto refresh every 60 seconds (60000 ms)
st_autorefresh(interval=60000, key="btc_refresh")

st.title("🧠 BTC AI Trading Assistant")
st.caption("4H Bias | 1H Execution | Continuation Model")

df_1h, df_4h = get_btc_data()

df_1h = detect_swings(df_1h)
df_4h = detect_swings(df_4h)

df_1h = classify_structure(df_1h)
df_4h = classify_structure(df_4h)

bias_4h = determine_bias(df_4h)
alignment = check_alignment(df_1h, bias_4h)

break_confirmed = recent_break_structure(df_1h)
volume_boost = volume_expansion(df_1h)

score = calculate_trade_score(
    bias_4h,
    alignment,
    break_confirmed,
    volume_boost
)

if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

if score >= 5 and not st.session_state.alert_sent:
    send_telegram_alert(message)
    st.session_state.alert_sent = True

if score < 5:
    st.session_state.alert_sent = False

if score >= 5:
    message = f"""
🚨 BTC TRADE SIGNAL 🚨

4H Bias: {bias_4h}
1H Alignment: {alignment}
Trade Score: {score}/6

Check dashboard for entry.
"""
    send_telegram_alert(message)

continuation_setup = None
if bias_4h == "Bullish" and alignment:
    continuation_setup = detect_bullish_continuation(df_1h)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("4H Bias", bias_4h)

with col2:
    st.metric("1H Alignment", alignment)

with col3:
    st.metric("Trade Score", f"{score}/6")

if score >= 5:
    st.success("🔥 HIGH PROBABILITY SETUP")
elif score >= 3:
    st.warning("👀 WATCHLIST")
else:
    st.error("❌ NO TRADE")

if continuation_setup:
    st.subheader("🚀 Bullish Continuation Setup")
    st.write(f"**Entry:** {continuation_setup['entry']}")
    st.write(f"**Stop Loss:** {continuation_setup['stop_loss']}")
    st.write(f"**Take Profit:** {continuation_setup['take_profit']}")
    st.write(f"**Risk Reward:** 1:{continuation_setup['risk_reward']}")
else:
    st.info("No valid continuation entry yet.")

st.caption("Auto-refresh page manually for now (next phase = auto refresh)")
