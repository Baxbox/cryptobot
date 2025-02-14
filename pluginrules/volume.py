volume_multiplier = 2  # Requires volume to double

def should_trade(symbol, price, current_volume, average_volume):
    """Volume Surge: Buy if volume is 2x higher than average, Sell if it drops."""
    if current_volume >= average_volume * volume_multiplier:
        return "buy"
    elif current_volume < average_volume:
        return "sell"
    return None
