<h1>🚀 BaxBoxBot</h1>
<p>A <b>Solana-based crypto trading bot</b> that dynamically loads trading strategies, executes buy/sell orders based on real-time price data, and supports <b>alternate strategies</b> when the primary strategy fails or succeeds.</p>

<hr>

<h2>📌 Features</h2>
<ul>
    <li>✅ Supports <b>multiple wallets</b> and tokens</li>
    <li>✅ Uses <b>dynamic trading strategies</b> from the <code>pluginrules/</code> folder</li>
    <li>✅ <b>Alternate strategies</b>:
        <ul>
            <li>Switch to another strategy <b>if the primary fails</b></li>
            <li>Change to a new strategy <b>after a successful trade</b></li>
        </ul>
    </li>
    <li>✅ Automatically fetches <b>live token prices</b> from <b>Jupiter Aggregator</b></li>
    <li>✅ Modular and <b>easily extendable</b> with custom trading strategies</li>
</ul>

<hr>

<h2>📥 Installation</h2>
<h3>1️⃣ Set up a Python virtual environment (optional but recommended)</h3>
<pre>
<code>
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code>
</pre>

<h3>2️⃣ Install required dependencies</h3>
<pre>
<code>
pip install -r requirements.txt
</code>
</pre>

<h3>3️⃣ Configure your wallets and trading strategies</h3>
<p>Edit <b><code>config.json</code></b> to add your wallets, tokens, and trading strategies.</p>

<hr>

<h2>⚙️ Configuration (<code>config.json</code>)</h2>
<p>BaxBoxBot reads trading rules from <b><code>config.json</code></b>.</p>

<h3>Example:</h3>
<pre>
<code>
{
    "wallets": [
        {
            "name": "Brian",
            "wallet_secret": "suit space dentist habit gossip enter begin tide transfer group fine run",
            "tokens": [
                {
                    "symbol": "DEEP",
                    "mint_id": "hTRDn7zE5tDHRnjj6Qms2WG1zEGv9ii6AiwfgbFpump",
                    "buy_price": 0.0,
                    "strategy": {
                        "primary": "2x",
                        "on_fail": "momentum",
                        "on_success": "grid"
                    }
                },
                {
                    "symbol": "TRUMP",
                    "mint_id": "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN",
                    "buy_price": 1.5,
                    "strategy": {
                        "primary": "rsi",
                        "on_fail": "volume"
                    }
                }
            ]
        }
    ]
}
</code>
</pre>

<h3>🔄 Strategy Settings</h3>
<ul>
    <li><b><code>primary</code></b> → The main strategy to use</li>
    <li><b><code>on_fail</code></b> → Used if the primary strategy <b>fails</b></li>
    <li><b><code>on_success</code></b> → Used when the primary <b>executes a successful trade</b></li>
</ul>

<hr>

<h2>🚀 How It Works</h2>
<ol>
    <li>The bot <b>fetches real-time token prices</b> from <b>Jupiter Aggregator</b></li>
    <li>It <b>loads the trading strategy</b> specified in <code>config.json</code></li>
    <li>If the <b>primary strategy fails</b>, it switches to <code>on_fail</code></li>
    <li>If a <b>trade executes successfully</b>, it switches to <code>on_success</code></li>
    <li>The bot continuously <b>monitors and executes trades</b> every <b>60 seconds</b></li>
</ol>

<hr>

<h2>📌 Available Trading Strategies</h2>
<table>
    <tr>
        <th>Strategy Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td><b>2x</b></td>
        <td>Sells when price reaches <b>2X</b> the buy price</td>
    </tr>
    <tr>
        <td><b>forever</b></td>
        <td>Keeps trading continuously within a <b>10% range</b></td>
    </tr>
    <tr>
        <td><b>trailing</b></td>
        <td>Sells if price drops <b>5% from the highest</b> after buying</td>
    </tr>
    <tr>
        <td><b>mean</b></td>
        <td>Buys when price drops <b>5% below the moving average</b>, sells when it rises <b>5% above</b></td>
    </tr>
    <tr>
        <td><b>momentum</b></td>
        <td>Buys when price increases <b>3% in a short time</b>, sells if it drops</td>
    </tr>
    <tr>
        <td><b>grid</b></td>
        <td>Places <b>buy/sell orders</b> at set price intervals (e.g., every <b>5%</b>)</td>
    </tr>
    <tr>
        <td><b>rsi</b></td>
        <td>Uses <b>Relative Strength Index (RSI)</b> to determine buy/sell points</td>
    </tr>
    <tr>
        <td><b>time</b></td>
        <td>Buys and sells <b>at fixed time intervals</b></td>
    </tr>
    <tr>
        <td><b>volume</b></td>
        <td>Buys when <b>trading volume spikes</b>, sells when it drops</td>
    </tr>
    <tr>
        <td><b>custom</b></td>
        <td>Sells when price reaches a <b>custom target percentage gain</b></td>
    </tr>
</table>

<hr>

<h2>🔧 Adding Custom Strategies</h2>
<p>To create a <b>new strategy</b>, add a <code>.py</code> file inside <code>pluginrules/</code> and define a function:</p>
<pre>
<code>
def should_trade(symbol, price, buy_price):
    if price <= buy_price:
        return "buy"
    elif price >= buy_price * 1.5:
        return "sell"
    return None
</code>
</pre>
<p>Then, update <b><code>config.json</code></b> to use the new strategy.</p>

<hr>

<h2>▶ Running the Bot</h2>
<p>Start the bot with:</p>
<pre>
<code>
python3 baxboxbot.py
</code>
</pre>
<p>The bot will continuously monitor prices and execute trades every <b>60 seconds</b>.</p>

<hr>

<h2>📅 Planned Features</h2>
<ul>
    <li>🚀 <b>Stop-loss and take-profit settings</b></li>
    <li>🚀 <b>Machine-learning-based trading strategies</b></li>
    <li>🚀 <b>Multi-chain support (Ethereum, BSC, etc.)</b></li>
    <li>🚀 <b>Discord/Telegram alerts for trades</b></li>
</ul>

<hr>

<h2>🤝 Contributing</h2>
<p>Want to improve <b>BaxBoxBot</b>? Feel free to submit <b>pull requests</b> or <b>new strategy ideas</b>!</p>

<hr>

<h2>📄 License</h2>
<p>This project is <b>open-source</b> and distributed under the <b>MIT License</b>.</p>

<hr>

<h2>📧 Contact & Support</h2>
<p>For any questions or issues, feel free to <b>open a GitHub issue</b> or reach out!</p>
