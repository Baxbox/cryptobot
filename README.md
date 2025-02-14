
# **BaxBoxBot**  
A **Solana-based crypto trading bot** that dynamically loads trading strategies and executes buy/sell orders based on real-time price data.  

## **Features**
✅ Supports multiple wallets and token lists.  
✅ Uses **dynamic trading strategies** from the `pluginrules/` folder.  
✅ Supports **different strategies per token** (e.g., **2X Rule, Momentum Rule, RSI Rule**).  
✅ Automatically fetches live token prices from **Jupiter Aggregator**.  
✅ Modular and **easily extendable** with custom trading strategies.  

---

## **Installation**
### **1. Set up a Python virtual environment (optional but recommended)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **2. Install required dependencies**
```sh
pip install -r requirements.txt
```

### **3. Configure your wallets and trading strategies**
Edit **`config.json`** to add your wallets, tokens, and trading strategies.

Example:
```json
{
    "wallets": [
        {
            "name": "My Wallet",
            "wallet_secret": [128, 45, 76, ...],
            "tokens": [
                {
                    "symbol": "SOL",
                    "buy_price": 80.0,
                    "strategy": "2x"
                },
                {
                    "symbol": "RAY",
                    "buy_price": 1.5,
                    "strategy": "momentum"
                }
            ]
        }
    ]
}
```

---

## **How It Works**
1. The bot **fetches real-time token prices** from **Jupiter Aggregator**.
2. It dynamically **loads the trading strategy** specified in `config.json`.
3. Each strategy **determines if a buy or sell order should be executed**.
4. The bot continuously **monitors and executes trades** every 60 seconds.

---

## **Available Trading Strategies**
BaxBoxBot supports **various trading strategies**, stored in `pluginrules/`.

| Strategy Name       | Description |
|--------------------|-------------|
| **2x** | Sells when price reaches **2X** the buy price. |
| **forever** | Keeps trading continuously within a **10% range**. |
| **trailing** | Sells if price drops **5% from the highest** after buying. |
| **mean** | Buys when price drops **5% below the moving average**, sells when it rises **5% above**. |
| **momentum** | Buys when price increases **3% in a short time**, sells if it drops. |
| **grid** | Places **buy/sell orders** at set price intervals (e.g., every **5%**). |
| **rsi** | Uses **Relative Strength Index (RSI)** to determine buy/sell points. |
| **time** | Buys and sells **at fixed time intervals**. |
| **volume** | Buys when **trading volume spikes**, sells when it drops. |
| **custom** | Sells when price reaches a **custom target percentage gain**. |

---

## **Adding Custom Strategies**
To create a **new strategy**, add a `.py` file inside `pluginrules/` and define a function:
```python
def should_trade(symbol, price, buy_price):
    if price <= buy_price:
        return "buy"
    elif price >= buy_price * 1.5:
        return "sell"
    return None
```
Then, update **`config.json`** to use the new strategy.

---

## **Running the Bot**
Start the bot with:
```sh
python3 baxboxbot.py
```

The bot will continuously monitor prices and execute trades every **60 seconds**.

---

## **Planned Features**
🚀 **Stop-loss and take-profit settings**  
🚀 **Machine-learning-based trading strategies**  
🚀 **Multi-chain support (Ethereum, BSC, etc.)**  
🚀 **Discord/Telegram alerts for trades**  

---

## **Contributing**
Want to improve **BaxBoxBot**? Feel free to submit **pull requests** or **new strategy ideas**!

---

This README gives **clear setup instructions**, explains the **trading strategies**, and makes it easy to extend the bot. 🚀 Let me know if you need any refinements!