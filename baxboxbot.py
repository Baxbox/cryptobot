import json
import time
import requests
# pip install solana==0.28.0
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair

# Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
JUPITER_API_URL = "https://quote-api.jup.ag/v6"
RULES_DIR = "pluginrules"

# Load wallets and trading rules
with open("config.json", "r") as f:
    config = json.load(f)

solana_client = Client(SOLANA_RPC_URL)

def get_token_price(symbol):
    """Fetch the token price from Jupiter Aggregator."""
    response = requests.get(f"{JUPITER_API_URL}/price?ids={symbol}")
    data = response.json()
    return data.get("data", {}).get(symbol, {}).get("price", None)

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

def buy_or_sell(symbol, price, strategy_name, buy_price):
    """Wrapper function to return buy/sell decision based on the selected strategy."""
    strategy_module = load_strategy(strategy_name)
    if strategy_module and hasattr(strategy_module, "should_trade"):
        return strategy_module.should_trade(symbol, price, buy_price)
    return None  # No trade if no valid strategy is found

def check_trading_conditions(wallet_config):
    """Check trading conditions for a given wallet and execute trades."""
    for token in wallet_config["tokens"]:
        symbol = token["symbol"]
        strategy_name = token.get("strategy")  # Load strategy from config
        buy_price = token.get("buy_price", 0)  # Reference price for strategy
        price = get_token_price(symbol)

        if price is None or not strategy_name:
            continue

        decision = buy_or_sell(symbol, price, strategy_name, buy_price)
        if decision in ["buy", "sell"]:
            execute_trade(wallet_config["wallet_secret"], symbol, decision)

def execute_trade(wallet_secret, symbol, trade_type):
    """Simulated trade execution."""
    wallet = Keypair.from_secret_key(bytes(wallet_secret))
    print(f"{trade_type.upper()} order executed for {symbol} in wallet {wallet.public_key()}")

if __name__ == "__main__":
    while True:
        for wallet_config in config["wallets"]:
            check_trading_conditions(wallet_config)
        time.sleep(60)
