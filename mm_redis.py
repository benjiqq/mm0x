"""
export PYTHONPATH=/Users/ben/project_0x/pymaker:/Users/ben/project_0x/pyexchange:/Users/ben/github/web3.py:/Users/ben/github/archon-dex
export PRIVATEKEY='0x';
export INFURA_KEY='...';
"""

import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance
from tokens import *

import requests
import json
from web3 import Web3, HTTPProvider
import pymongo
import os
import redis
host = "127.0.0.1"
port = 6379
redis_client = redis.Redis(host=host, port=port)


#syms = ["USDC", "TUSD", "BAT", "CVC", "DNT", "LOOM", "MANA", "REP"]

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()
print (myaddr)




def show_maker_fills():
    fills = radar.get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    for fill in maker_fills:
        print (fill)

def set_open_orders():
    print ("set_open_orders")
    orders = radar.get_orders(address = myaddr)
    #print (orders)
    open_orders = list(filter(lambda x: x["state"]=='OPEN',orders))
    redis_client.set("open_orders",json.dumps(open_orders))
    with open('orders.json', 'w') as outfile:
        json.dump(open_orders, outfile)

def set_balance():
    bal = get_balance(myaddr) 
    redis_client.set("balance",json.dumps(bal))   
    with open('balance.json', 'w') as outfile:
        json.dump(bal, outfile)    

if __name__=='__main__':
    set_open_orders()
    set_balance()
    