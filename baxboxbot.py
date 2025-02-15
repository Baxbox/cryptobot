import json
import time
import requests
import sys
import os
from datetime import datetime
# pip install solana==0.28.0
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair
import db

# Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
JUPITER_API_URL = "https://api.jup.ag/price/v2"
RULES_DIR = "pluginrules"
CYCLE_SEC = 60

# Load wallets and trading rules
with open("config.json", "r") as f:
    config = json.load(f)

solana_client = Client(SOLANA_RPC_URL)

def get_token_price(mint_id):
    """Fetch the token price from Jupiter Aggregator."""
    url = f"{JUPITER_API_URL}?ids={mint_id}"
    response = requests.get(url)
    data = response.json()
    # Extract the price and convert to float
    price_str = data.get("data", {}).get(mint_id, {}).get("price", None)
    return float(price_str) if price_str else None  # Convert to float safely

def load_strategy(strategy_name):
    """Dynamically load a trading strategy module from the pluginrules directory."""
    rule_file = f"{strategy_name.lower()}_rule.py"
    rule_path = os.path.join(RULES_DIR, rule_file)

    if not os.path.exists(rule_path):
        print(f"Strategy {strategy_name} not found. Skipping...")
        return None

    spec = importlib.util.spec_from_file_location("rule_module", rule_path)
    rule_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rule_module)
    return rule_module

def buy_or_sell(symbol, usd_price, strategy_name, buy_price):
    """Wrapper function to return buy/sell decision based on the selected strategy."""
    strategy_module = load_strategy(strategy_name)
    if strategy_module and hasattr(strategy_module, "should_trade"):
        return strategy_module.should_trade(symbol, usd_price, buy_price)
    return None  # No trade if no valid strategy is found

def check_trading_conditions(wallet_config):
    """Check trading conditions for a given wallet and execute trades."""
    for token in wallet_config["tokens"]:
        symbol = token["symbol"]
        mint_id = token["mint_id"]
        strategy_name = token.get("strategy")  # Load strategy from config
        buy_price = token.get("buy_price", 0)  # Reference price for strategy
        usd_price = get_token_price(mint_id)
        print(symbol)
        print(usd_price)
        if usd_price is None or not strategy_name:
            continue

        decision = buy_or_sell(symbol, usd_price, strategy_name, buy_price)
        if decision in ["buy", "sell"]:
            execute_trade(wallet_config["wallet_secret"], symbol, decision, strategy_name, usd_price, coin_price)

def execute_trade(wallet_secret, symbol, trade_type, strategy, usd_price, coin_price):
    """Simulated trade execution."""
    wallet = Keypair.from_secret_key(bytes(wallet_secret))
    print(f"{trade_type.upper()} order executed for {symbol} in wallet {wallet.public_key()}")
    db.create_trade(symbol,trade_type,usd_price,coin_price,strategy,wallet.public_key())
    
if __name__ == "__main__":
    while True:
        for wallet_config in config["wallets"]:
            check_trading_conditions(wallet_config)
        time.sleep(CYCLE_SEC)
