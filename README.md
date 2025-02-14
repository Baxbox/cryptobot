# BaxBoxBot

## Overview
This is a simple automated trading bot for **Solana-based tokens**, designed to monitor prices and execute trades based on predefined conditions. The bot supports multiple wallets, allowing different users to have their own lists of coins and trading rules. This is currently a prototype non-functioning.

## Features
- 🪙 **Supports Multiple Wallets** – Manage multiple Solana wallets with unique trading strategies.
- 📈 **Price Monitoring** – Fetches real-time token prices using the **Jupiter API**.
- 🤖 **Automated Trading** – Buys and sells tokens when price conditions are met.
- 🔄 **Continuous Execution** – Runs in a loop, checking for trades every 60 seconds.
- 🔧 **Configurable Settings** – All settings (wallets, tokens, buy/sell rules) are stored in `config.json`.

## Installation

### 1. **Clone the Repository**
```bash
git clone https://github.com/Baxbox/cryptobot.git
cd cryptobot
```

### 2. **Set Up a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate    # Windows
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

## Configuration

### 1. **Edit `config.json`**
Define your wallets, tokens, and price triggers:
```json
{
    "wallets": [
        {
            "name": "My Wallet",
            "wallet_secret": [128, 45, 76, ...],
            "tokens": [
                {"symbol": "SOL", "buy_price": 80.0, "sell_price": 150.0},
                {"symbol": "RAY", "buy_price": 1.2, "sell_price": 3.5}
            ]
        }
    ]
}
```

### 2. **Run the Bot**
```bash
python baxboxbot.py
```

## Notes
- Make sure your wallet secret key is **stored securely**.
- Use a private RPC service for better performance if needed.
- You can modify the `time.sleep(60)` value in the script to adjust the frequency of price checks.

## License
This project is open-source under the **MIT License**.

🚀 Happy Trading!

