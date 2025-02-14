def should_trade(symbol, price, buy_price):
    """Forever rule: Continuously buys 10% below buy_price and sells 10% above."""
    buy_threshold = buy_price * 0.9
    sell_threshold = buy_price * 1.1

    if price <= buy_threshold:
        return "buy"
    elif price >= sell_threshold:
        return "sell"
    return None
