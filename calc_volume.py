"""
utility to analyse maker-transactions on 0x
"""

from archondex.relay.radar import *
from archondex.binance_utils import *
import requests
import json
from web3 import Web3, HTTPProvider
import datetime
from tokens import *

privateKey = os.environ['PRIVATEKEY']
INFURA_KEY = os.environ['INFURA_KEY']

w3 = Web3(HTTPProvider("https://mainnet.infura.io/" + INFURA_KEY))
acct = w3.eth.account.privateKeyToAccount(privateKey)
myaddr = (acct.address).lower()
#print (myaddr)



def get_ethusd_map():
    """ get candle and convert to dict of daily prices """ 
    ethusdt = get_ethusdt()
    #print (ethusdt)
    d = {}
    for x in ethusdt[-10:]:
        ts = x[0]
        binance_ts = datetime.datetime.strftime(ts,'%Y-%m-%d')
        d[binance_ts] = float(x[4])
    return d

def show_maker_fills():
    print ('volume maker analysis for ' + myaddr)
    eth_usd_map = get_ethusd_map()
    #print (eth_usd_map)
    eth_usd_map["2019-02-20"] = 142.71
    eth_usd_map['2019-02-10'] = 100
    
    fills = get_fills(address = myaddr)
    maker_fills = list(filter(lambda x: x["makerAddress"]==myaddr,fills))
    taker_fills = list(filter(lambda x: x["makerAddress"]!=myaddr,fills))
    
    #print ("*** date\tusd_volume \t eth_usd\t eth_volume\t volume\t filltype \t symbol***")
    print ("*** date\tusd_volume \tfilltype \t symbol***")
    total_usd = 0

    maker_fills.reverse()
    print (myaddr)
    txhashes = set()
    for fill in maker_fills[:]:
        print (fill) 
        ta = fill["takerAddress"]
        if ta==myaddr: print ("selftrade! ",fill)        
        
        #print (fill)
        fill_type = fill["type"]
        z = lambda x: "BUY" if x=="SELL" else "SELL"
        maker_type = z(fill_type)
        t = fill["timestamp"]
        bt = fill["baseTokenAddress"]
        sym = tokens[bt]
        ts = datetime.datetime.utcfromtimestamp(t)
        tsfd = datetime.datetime.strftime(ts,'%Y-%m-%d')
        #if ts.day <= 10: continue
        #print (ts)
        try:
            eth_usd = eth_usd_map[tsfd]
        except:
            continue
        if ts.day <= 19: continue
        #print (fill)
        eth_volume = float(fill["filledQuoteTokenAmount"])
        v = float(fill["filledBaseTokenAmount"])
        p = eth_volume/v
        #print (eth_volume,v,p)
        usd_volume = eth_usd * eth_volume
        #print (ts.day)
        if ts.day >= 1:
            th = fill["transactionHash"]
            txhashes.add(th)
            print (tsfd,"\t",round(usd_volume,2),"\t",maker_type,"\t",sym,"\t",p)
            total_usd += usd_volume
    print ("maker_fills ",len(maker_fills))            
    print ("taker_fills ",len(taker_fills))            
    print ("total_usd ",round(total_usd,0))
    print (len(txhashes))
    #print (txhashes)

    #print (taker_fills)
    #taker_fills = list(filter(lambda x: x["makerAddress"]!=myaddr,fills))

        
        

show_maker_fills()