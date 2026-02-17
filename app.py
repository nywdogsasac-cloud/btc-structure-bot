from data_engine import get_btc_data
from structure_engine import detect_bullish_continuation

from structure_engine import (
    detect_swings,
    classify_structure,
    determine_bias,
    check_alignment,
    volume_expansion,
    recent_break_structure,
    calculate_trade_score
)

df_1h, df_4h = get_btc_data()

# Detect swings
df_1h = detect_swings(df_1h)
df_4h = detect_swings(df_4h)

# Classify structure
df_1h = classify_structure(df_1h)
df_4h = classify_structure(df_4h)

# Bias + Alignment
bias_4h = determine_bias(df_4h)
alignment = check_alignment(df_1h, bias_4h)

# Additional conditions
break_confirmed = recent_break_structure(df_1h)
volume_boost = volume_expansion(df_1h)

# Score
score = calculate_trade_score(
    bias_4h,
    alignment,
    break_confirmed,
    volume_boost
)

continuation_setup = None

if bias_4h == "Bullish" and alignment:
    continuation_setup = detect_bullish_continuation(df_1h)

# Classification
if score >= 5:
    state = "HIGH PROBABILITY SETUP"
elif score >= 3:
    state = "WATCHLIST"
else:
    state = "NO TRADE"

print("==== BTC AI TRADE REPORT ====")
print(f"4H Bias: {bias_4h}")
print(f"1H Alignment: {alignment}")
print(f"Trade Score: {score}/6")
print(f"State: {state}")

if continuation_setup:
    print("\n🚀 BULLISH CONTINUATION SETUP DETECTED")
    print(f"Entry: {continuation_setup['entry']}")
    print(f"Stop Loss: {continuation_setup['stop_loss']}")
    print(f"Take Profit: {continuation_setup['take_profit']}")
    print(f"RR: 1:{continuation_setup['risk_reward']}")
else:
    print("\nNo valid continuation entry yet.")

