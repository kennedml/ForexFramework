#!/usr/bin/env python

from backtester import *
import settings
from strategy import TestStrategy
from datahandler import HistoricPriceHandler


def main():
    # Trade on GBP/USD and EUR/USD
    pairs = ["EURUSD"]
    
    # This strategy has no params to pass
    strategy_params = {}
   
    #Create and execute the backtest
    backtester = Backtester(pairs, HistoricPriceHandler, TestStrategy, strategy_params)
    print "Calling backtest.simulate_trading()"
    backtester.simulate_trading()

if __name__ == "__main__":
    main()
