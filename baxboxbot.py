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
import importlib
from solders.keypair import Keypair as SolderKeypair
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from solders.keypair import Keypair as SolderKeypair

# Configuration
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
SOL_MINT_ID = "So11111111111111111111111111111111111111112"
JUPITER_API_URL = "https://api.jup.ag/price/v2"
RULES_DIR = "pluginrules"
CYCLE_SEC = 60

# Load wallets and trading rules
with open("config.json", "r") as f:
    config = json.load(f)

solana_client = Client(SOLANA_RPC_URL)

def get_token_price(price_data,mint_id):
    # Extract the price and convert to float
    #print(price_data)
    price_str = price_data["data"].get(mint_id, {}).get("price")
    return float(price_str) if price_str else None  # Convert to float safely

def get_token_data(mint_id):
    """Fetch the token data from Jupiter Aggregator."""
    url = f"{JUPITER_API_URL}?ids={mint_id}&showExtraInfo=true"
    response = requests.get(url)
    return response.json()
    
def load_strategy(strategy_name):
    """Dynamically load a trading strategy module from the pluginrules directory."""
    rule_file = f"{strategy_name.lower()}.py"
    rule_path = os.path.join(RULES_DIR, rule_file)
    #print(rule_path)

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
        print("Coin: "+symbol)
        mint_id = token["mint_id"]
        strategy_name = token.get("strategy")
        print("Strategy: "+strategy_name)
        buy_price = token.get("buy_price", 0)
        print("Buy Price: "+str(buy_price))
        usd_price = get_token_price(get_token_data(mint_id), mint_id)
        print("Coin Price: "+ str(usd_price))
        if usd_price is None or not strategy_name:
            continue
        
        coin_price = usd_price  # Store USD price as `coin_price` to avoid redundant API calls

        decision = buy_or_sell(symbol, usd_price, strategy_name, buy_price)
        if decision in ["buy", "sell"]:
            print("Decision: " + decision)
            execute_trade(wallet_config["wallet_secret"], symbol, decision, strategy_name, usd_price, mint_id, coin_price)
        print("------------")
def load_wallet_from_mnemonic(mnemonic):
    """Load Solana wallet from a mnemonic phrase."""
    #print(f"🔍 Mnemonic received: {mnemonic}")  # Debugging line
    
    if isinstance(mnemonic, list):
        mnemonic = " ".join(mnemonic)  # Convert list to string if needed

    words = mnemonic.split()  # Convert to list
    #print(f"✅ Word Count: {len(words)}")  # Debugging: Print number of words

    if len(words) not in [12, 15, 18, 21, 24]:
        raise ValueError(f"❌ Invalid mnemonic length: {len(words)} words")

    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()  
    bip44_sol = Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA).DeriveDefaultPath()
    private_key_bytes = bip44_sol.PrivateKey().Raw().ToBytes()

    # ✅ Use from_seed() instead of from_bytes()
    return SolderKeypair.from_seed(private_key_bytes)


def execute_trade(wallet_secret, symbol, trade_type, strategy, usd_price, mint_id, coin_price):
    """Simulated trade execution."""
    #print(wallet_secret)  # Debugging: Check wallet mnemonic
    wallet = load_wallet_from_mnemonic(wallet_secret)  # Convert mnemonic to keypair
    print(f"{trade_type.upper()} order executed for {symbol} in wallet {wallet.pubkey()}")

    db.create_trade(symbol, trade_type, usd_price, coin_price, strategy, str(wallet.pubkey()))

if __name__ == "__main__":
    while True:
        for wallet_config in config["wallets"]:
            wallet_name = wallet_config.get("name", "Unnamed Wallet")  # Get wallet name, with a fallback
            print(f"Wallet: {wallet_name}")
            print("##############################")
            check_trading_conditions(wallet_config)
        time.sleep(CYCLE_SEC)
