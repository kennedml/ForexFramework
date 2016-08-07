#!/usr/bin/env python

# File Name: backtester.py
# Creation Date: Jul-30-2016
# Last Modified: Aug-05-2016
# Description: Encapsulates the settings and components for carrying out
#              an event-driven backtest for a FOREX pair


# Python 3 uses slightly different imports. Catch either
try:
    import Queue as queue
except ImportError:
    import queue

import time
import sys

# We need access to the settings file in the main dir
#sys.path.append('../')
import settings
import datahandler
import strategy

class Backtester(object):
    
    def __init__(self, pairs, data_handler, strategy, strategy_params):

        self.pairs = pairs
        self.events = queue.Queue()
        self.ticker = data_handler(self.pairs, self.events)
        self.strategy_params = strategy_params
        
        # **kwargs will give you all keyword arguments except for those
        # corresponding to a formal parameter as a dictionary.
        self.strategy = strategy(self.pairs, self.events, **self.strategy_params)
        
        self.heartbeat = 0 
        self.max_iters = 1000000
    
    def _run_backtest(self):
        """
        Carries out a while loop that polls the 
        events queue and directs each event to either the
        strategy object. The loop will then pause for a 
        "heartbeat" (heartbeat should be equal to 0 for backtesting) 
        and continue until the max iterations is reached
        """
        print("Running Backtest...")
        iters = 0
        while iters < self.max_iters and self.ticker.continue_backtest:
            try:
                event = self.events.get(False)
            except queue.Empty:
                self.ticker.stream_next_tick()
            else:
                if event is not None:
                    if event.type == 'TICK':
                        self.strategy.calculate_signals(event)
                # TODO check if other types of events exist
            time.sleep(self.heartbeat)
            iters += 1

    def _output_performance(self): # TODO
        """
        Outputs the strategy performance from the backtest.
        """
        pass

    def simulate_trading(self):
        """
        Simulates the backtest
        """
        self._run_backtest()
        print("Backtest complete.")

