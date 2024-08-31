#!/usr/bin/python3
import requests
import hmac
import hashlib
from string import Template
import time
from urllib.parse import urljoin, urlencode
from decimal import Decimal
import os

key_sec = ""
key_pub = ""

url_api_balance = "https://api.binance.com/api/v3/account"
url_api_price = "https://api.binance.com/api/v3/ticker/price"
url_api_order = "https://api.binance.com/api/v3/order"
url_api_info = "https://api.binance.com/api/v3/exchangeInfo"
url_order_book = "https://api.binance.com/api/v3/depth"
def buy(typ, kol, sym):
    tim = int(time.time() * 1000)
    params_order = {
            "symbol": sym,
            "side": typ,
            "type": "MARKET",
            "quantity": kol,
            "timestamp": tim,
            "recvWindow": 50000
            }
    query_order = urlencode(params_order)
    params_order["signature"] = hmac.new(key_sec.encode('utf-8'), query_order.encode('utf-8'), hashlib.sha256).hexdigest()
    return requests.post(url_api_order, params=params_order, headers={"X-MBX-APIKEY": key_pub})

def price(sym):
    return float((requests.get(url_api_price, params={"symbol": sym})).text.split("\"")[7])

def order_book(sym, buy_or_sell):
    
    if buy_or_sell == "b":
        return requests.get(url_order_book, params={"symbol": sym}).text.split("asks")[1].split('"')
    if buy_or_sell == "s":
        return requests.get(url_order_book, params={"symbol": sym}).text.split("bids")[1].split('"')

def balance(sym):
    tim = int(time.time() * 1000)
    params_balance = {
            "timestamp": tim,
            "recvWindow": 50000
            }
    query_balance = urlencode(params_balance)
    params_balance["signature"] = hmac.new(key_sec.encode('utf-8'), query_balance.encode('utf-8'), hashlib.sha256).hexdigest()
    req = requests.get(url_api_balance, params=params_balance, headers={"X-MBX-APIKEY": key_pub})
    return (req.text.split(sym)[1].split('"')[4])


def fee(b_mon):
    return b_mon - (b_mon / 100 * 0.075)

def crug_1(bal_usdt, price1, price2, price3):
    bal_sym1 = bal_usdt / price1
    bal_sym2 = fee(bal_sym1) / price2
    bal_sym3 = fee(bal_sym2) * price3
    return fee(bal_sym3)

def crug_2(bal_usdt, price1, price2, price3):
    bal_sym1 = bal_usdt / price1
    bal_sym2 = fee(bal_sym1) * price2
    bal_sym3 = fee(bal_sym2) * price3
    return fee(bal_sym3)


while True:

    ogran = int(((requests.get(url_api_info)).headers)['x-mbx-used-weight'])
    if ogran > 1000:
        print("danger: BAN")
        break
    
    
    bal_usd = 1000 #balance("USDT")
    def crug_check(sym_usdt, sym_btc, btc_or_eth):
        o_sym_usdt_buy = order_book(sym_usdt, "b")
        o_sym_btc_buy = order_book(sym_btc, "b")
        o_btc_usdt_buy = order_book("BTCUSDT", "b")
        o_eth_usdt_buy = order_book("ETHUSDT", "b")
        o_btc_usdt_sell = order_book("BTCUSDT", "s")
        o_sym_btc_sell = order_book(sym_btc, "s")
        o_sym_usdt_sell = order_book(sym_usdt, "s")

        if btc_or_eth == "btc":
            crug_1_u = crug_2(100, float(o_sym_usdt_buy[2]), float(o_sym_btc_sell[2]), float(o_btc_usdt_sell[2]))
            crug_1_b = crug_1(100, float(o_btc_usdt_buy[2]), float(o_sym_btc_buy[2]), float(o_sym_usdt_sell[2]))
            return round(crug_1_u, 2), round(crug_1_b, 2)
        if btc_or_eth == "eth":
            crug_1_u = crug_2(100, float(o_sym_usdt[2]))
            return round(crug_1_u, 2)


    print(crug_check("BNBUSDT", "BNBBTC", "btc"), crug_check("SOLUSDT", "SOLBTC", "btc"))
