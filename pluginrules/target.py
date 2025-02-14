def should_trade(symbol, price, buy_price, target_multiplier=1.5):
    """Custom Target Rule: Sells when price reaches a user-defined target."""
    target_price = buy_price * target_multiplier
    
    if price >= target_price:
        return "sell"
    return None