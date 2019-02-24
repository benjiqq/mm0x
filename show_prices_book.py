"""
aggressive market-maker

TODO
calculate midprice

bid = midprice - pip
ask = midprice + pip

"""

import archondex.relay.radar_public_api as radar_public
import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance
from tokens import *
from config_assets import asset_syms

from archondex.abstract_marketmaker import Marketmaker

def show():
    for symbol in asset_syms[1:]:
        #sym_bal = balances[symbol]
        #print (symbol,sym_bal)
        pair = symbol + "-WETH"
        bin_avg_price = binance.get_average(symbol)
        print ("bin_avg_price ",bin_avg_price)
        max_bal = 1.5

        book = radar_public.orderbook(pair)
        topbid = float(book["bids"][0]['price'])
        topask = float(book["asks"][0]['price'])
        midprice = (topbid+topask)/2
        print ("best bid",topbid)
        print ("best ask", topask)
        print ("midprice ",midprice)
                    
        bin_between = bin_avg_price > topbid and bin_avg_price < topask
        print ("bin_between ",bin_between)
           
if __name__=='__main__':
    show()