"""
export PYTHONPATH=/Users/ben/project_0x/pymaker:/Users/ben/project_0x/pyexchange:/Users/ben/github/web3.py:/Users/ben/github/archon-dex
export PRIVATEKEY='0x';
export INFURA_KEY='...';
"""

import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance

import requests
import json
from web3 import Web3, HTTPProvider
import pymongo
import os

#syms = ["USDC", "TUSD", "BAT", "CVC", "DNT", "LOOM", "MANA", "REP"]

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()
print (myaddr)

tokens = {"0x1985365e9f78359a9b6ad760e32412f4a445e862":"REP",
"0x0d8775f648430679a709e98d2b0cb6250d2887ef":"BAT",
"0x0f5d2fb29fb7d3cfee444a200298f468908cc942":"MANA",
"0xa4e8c3ec456107ea67d3075bf9e3df3a75823db0":"LOOM",
"0x0abdace70d3790235af448c88547603b945604ea":"DNT",
"0x41e5560054824ea6b0732e656e3ad64e20e94e45":"CVC"}


def show_maker_fills():
    fills = radar.get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    for fill in maker_fills:
        print (fill)

def show_open_orders():
    print ("show_open_orders")
    orders = radar.get_orders(address = myaddr)
    #print (orders)
    open_orders = list(filter(lambda x: x["state"]=='OPEN',orders))
    #print (open_orders)
    print ('symbol\ttype\tprice\tquantity')
    for o in open_orders:
        #veth = o["remainingQuoteTokenAmount"]
        bt = o["baseTokenAddress"]
        s = tokens[bt]
        qty = round(float(o["remainingBaseTokenAmount"]),0)
        p = round(float(o["price"]),6)
        #print (o)
        print (s," ",o["type"],p," ",qty) #," ",veth)

    
def submit_order(order): 
    print ("submit order ",order)
    [otype, symbol, price, qty] = order
    order = radar.request_order(otype, symbol, price, qty)
    js_order = radar.prepare_order(acct, order)    
    print ("submitting >>>> ", js_order)
    response = requests.post("https://api.radarrelay.com/v2/orders", js_order, timeout=10.0)
    #response is empty
    print (response)
    
def show_bal():
    bal = get_balance(myaddr)        
    for k,v in bal.items():
        print (k,":",v)          

def submit_all_buy():
    """ standard bid """
    syms = ["BAT", "CVC", "DNT", "LOOM", "MANA", "REP"]
    zq = 0.0005

    for symbol in syms:
        avg_price = get_average(symbol)
        print ("avg ",symbol,":",avg_price)
        target_price = avg_price * (1-zq)
        target_bal_eth = 2
        qty = round(target_bal_eth/target_price,0)
        otype = "BUY"
        order = [otype, symbol, target_price, qty]
        print (order)
        submit_order(order)

def submit_all_sell():
    binance.set_averages()

    #symbol = "REP"
    bal = get_balance(myaddr)
    syms = ["BAT", "CVC", "DNT", "LOOM", "MANA", "REP"]
    #syms = ["CVC"]
    bal["CVC"] = 14025
    for symbol in syms:
        try:
            avg_price = binance.get_average(symbol)
            percent_bal = 0.7
            qty = bal[symbol]*percent_bal
            zq = 0.00
            target_price = avg_price * (1+zq)
            otype = "SELL"
            order = [otype, symbol, target_price, qty]
            print ("avg ",avg_price," =>",target_price)
            print (order)
            submit_order(order)
        except Exception as e:
            print (symbol," ",e)


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    args = parser.parse_args()
    print(args.action)
    if args.action == "submitbuy":
        submit_all_buy()
    elif args.action == "openorders":
        show_open_orders()
    elif args.action == "balances":
        show_bal()
    elif args.action == "submitsell":        
        submit_all_sell()   
    else:
        parser.print_help()
        