"""
aggressive market-maker

"""

import archondex.relay.radar_public_api as radar_public
import archondex.relay.radar as radar
import archondex.binance_avg as binance
from archondex.ethplorer import get_balance
from tokens import *
from config_assets import asset_syms

from archondex.abstract_marketmaker import Marketmaker
    

def book():
    print ("get book")
    pair = "REP-WETH"
    radar_public.show_orderbook(pair)

if __name__=='__main__':
    m = Marketmaker()
    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    args = parser.parse_args()
    print(args.action)
    if args.action == "openorders":
        m.show_open_orders()
    elif args.action == "balances":
        m.show_bal()
    elif args.action == "buy":
        m.submit_all_buy()
    else:
        parser.print_help()
    
    