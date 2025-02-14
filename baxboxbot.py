import json
import time
import requests
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.keypair import Keypair

# Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
JUPITER_API_URL = "https://quote-api.jup.ag/v6"

# Load wallets and trading rules
with open("config.json", "r") as f:
    config = json.load(f)

solana_client = Client(SOLANA_RPC_URL)

def get_token_price(symbol):
    """Fetch the token price from Jupiter Aggregator."""
    response = requests.get(f"{JUPITER_API_URL}/price?ids={symbol}")
    data = response.json()
    return data.get("data", {}).get(symbol, {}).get("price", None)

def check_trading_conditions(wallet_config):
    """Check trading conditions for a given wallet and execute trades."""
    for token in wallet_config["tokens"]:
        symbol = token["symbol"]
        price = get_token_price(symbol)
        if price is None:
            continue
        
        if price <= token["buy_price"]:
            execute_trade(wallet_config["wallet_secret"], symbol, "buy")
        elif price >= token["sell_price"]:
            execute_trade(wallet_config["wallet_secret"], symbol, "sell")

def execute_trade(wallet_secret, symbol, trade_type):
    """Simulated trade execution."""
    wallet = Keypair.from_secret_key(bytes(wallet_secret))
    print(f"{trade_type.upper()} order executed for {symbol} in wallet {wallet.public_key}")

if __name__ == "__main__":
    while True:
        for wallet_config in config["wallets"]:
            check_trading_conditions(wallet_config)
        time.sleep(60)
        