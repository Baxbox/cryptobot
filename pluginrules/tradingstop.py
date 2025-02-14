trailing_stop_percent = 0.05  # 5% trailing stop

def should_trade(symbol, price, buy_price, highest_price=None):
    """Trailing Stop Rule: Buy below buy_price, sell when price drops X% from peak."""
    if highest_price is None:
        highest_price = buy_price  # Initialize highest price

    if price <= buy_price:
        return "buy"
    
    if price > highest_price:
        highest_price = price  # Update highest price

    if price <= highest_price * (1 - trailing_stop_percent):
        return "sell"

    return None
