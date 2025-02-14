def should_trade(symbol, price, rsi_value):
    """RSI Rule: Buy if RSI < 30 (oversold), Sell if RSI > 70 (overbought)."""
    if rsi_value < 30:
        return "buy"
    elif rsi_value > 70:
        return "sell"
    return None
