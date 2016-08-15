#!/usr/bin/env python
from __future__ import print_function

import datetime
import os
import os.path
import re
import time

import numpy as np
import pandas as pd 

import settings
from event import TickEvent


class PriceHandler(object):
    """
    PriceHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a PriceHandler object is to output a set of
    candle "ticks" for each currency pair and place them into
    an event queue.
    
    Since a live strategy can only use a walk-forward event-based approach
    we will replicate that drip feed style for our historic feeds as well.
    """

    pass

class HistoricPriceHandler(PriceHandler):
    """
    HistoricPriceHandler is designed to read .pkl files created
    by create_ohlc.py script and stream the results provided to 
    the events queue
    """

    def __init__(self, pairs, events_queue):
        self.pairs = pairs
        self.events_queue = events_queue
        self.continue_backtest = True
        self.pickle = settings.PICKLE
        self.ticker_idx = 0
        self.dataframe = pd.read_pickle(settings.PICKLE)
        self.bid_open_data = []
        self.bid_close_data = []
        self.bid_low_data = []
        self.bid_high_data = []
        self.dates = []
        self.ask_open_data = []
        self.ask_close_data = []
        self.ask_low_data = []
        self.ask_high_data = []

        self._load_lists()
    
    def _load_lists(self):
        for row in self.dataframe.itertuples():
            dateTime, buyOpen, buyHigh, buyLow, buyClose, sellOpen, sellHigh, sellLow,sellClose = row
        
            if dateTime.dayofweek == 5:
                continue

            search = str(dateTime)
            g = re.search("(\d{4}-\d{2}-\d{2})", search)
            date = g.group(0)
            
            askOpen = float("{:.4f}".format(sellOpen))
            askHigh = float("{:.4f}".format(sellHigh))
            askLow = float("{:.4f}".format(sellLow))
            askClose = float("{:.4f}".format(sellClose))

            bidOpen = float("{:.4f}".format(buyOpen))
            bidHigh = float("{:.4f}".format(buyHigh))
            bidLow = float("{:.4f}".format(buyLow))
            bidClose = float("{:.4f}".format(buyClose))

            #candleHigh = float("{0:.4f}".format((buyHigh + sellHigh) / 2))
            #candleLow = float("{0:.4f}".format((buyLow + sellLow) / 2))
            #candleClose = float("{0:.4f}".format((buyClose + sellClose) / 2))
            #candleOpen = float("{0:.4f}".format((buyOpen + sellOpen) / 2))
            
            self.ask_open_data.append(askOpen)
            self.ask_high_data.append(askHigh)
            self.ask_low_data.append(askLow)
            self.ask_close_data.append(askClose)
            self.bid_open_data.append(bidOpen)
            self.bid_high_data.append(bidHigh)
            self.bid_low_data.append(bidLow)
            self.bid_close_data.append(bidClose)
            
            self.dates.append(dateTime)

    def stream_next_tick(self):
        """
        This method is called by the backtesting function outside
        of this class and places a single "TICK" event onto the queue
        """
        
        index = self.dates[self.ticker_idx]
        askOpen = self.ask_open_data[self.ticker_idx]
        askClose = self.ask_close_data[self.ticker_idx]
        askHigh = self.ask_high_data[self.ticker_idx]
        askLow = self.ask_low_data[self.ticker_idx]
        bidOpen = self.bid_open_data[self.ticker_idx]
        bidClose = self.bid_close_data[self.ticker_idx]
        bidHigh = self.bid_high_data[self.ticker_idx]
        bidLow = self.bid_low_data[self.ticker_idx]

        # Create the tick event for the queue
        tev = TickEvent(self.pairs[0], index, askOpen, askClose, askHigh,askLow, bidOpen, bidClose, bidHigh, bidLow)
        
        # Put the event into the queue
        self.events_queue.put(tev)
        
        # Increase ticker index
        self.ticker_idx += 1
        
        # Check to see if any more tick events exist
        if self.ticker_idx >= len(self.dates):
            self.continue_backtest = False
