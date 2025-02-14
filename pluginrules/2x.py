def should_trade(symbol, price, buy_price):
    """2X rule: Buy below buy_price, sell at 2X buy_price."""
    sell_price = buy_price * 2

    if price <= buy_price:
        return "buy"
    elif price >= sell_price:
        return "sell"
    return None
