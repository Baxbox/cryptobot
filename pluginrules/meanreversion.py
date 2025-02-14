def should_trade(symbol, price, buy_price, moving_average):
    """Mean Reversion: Buy when price < 95% of moving average, Sell when > 105%."""
    if price <= moving_average * 0.95:
        return "buy"
    elif price >= moving_average * 1.05:
        return "sell"
    return None
