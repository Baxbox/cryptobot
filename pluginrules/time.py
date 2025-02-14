import time

trade_interval = 3600  # 1 hour

def should_trade(symbol, price, last_trade_time):
    """Time-Based Rule: Trade every 1 hour."""
    current_time = time.time()
    if current_time - last_trade_time >= trade_interval:
        return "buy" if last_trade_time % 2 == 0 else "sell"  # Alternate buy/sell
    return None
