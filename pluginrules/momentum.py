momentum_percent = 0.03  # 3% increase within timeframe

def should_trade(symbol, price, buy_price, previous_price):
    """Momentum Rule: Buy if price rises 3% in last check, sell if price falls 3%."""
    if price >= previous_price * (1 + momentum_percent):
        return "buy"
    elif price <= previous_price * (1 - momentum_percent):
        return "sell"
    return None
