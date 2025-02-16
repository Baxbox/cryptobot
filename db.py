import sys
from datetime import datetime
from tinydb import TinyDB, Query

BOT_DB = "baxboxbot.json"
trade = Query()

def create_trade(symbol,trade_type,usd_price,coin_price,strategy,wallet):
    db = TinyDB(BOT_DB)
    now = datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    db.insert({"symbol":symbol,"strategy":strategy,"trade_type":trade_type,"usd_price":usd_price,"coin_price":coin_price,"datetime":now,"wallet":wallet})

def read_mean(min,symbol):
    pass

def read_trades(date,symbol,wallet):
    return db.search(trade.symbol == symbol,trade.wallet==wallet)
    
#sys.exit()