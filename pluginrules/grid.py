grid_spacing = 0.05  # 5% price spacing between grid levels

def should_trade(symbol, price, buy_price):
    """Grid Trading: Buy at every 5% drop, sell at every 5% rise from last buy."""
    if price <= buy_price * (1 - grid_spacing):
        return "buy"
    elif price >= buy_price * (1 + grid_spacing):
        return "sell"
    return None
