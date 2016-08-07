import copy

from event import SignalEvent


class TestStrategy(object):
    """
    A testing strategy that alternates between buying and selling
    a currency pair on every 5th tick. This is simply to test functionality
    and is not meant to be a profitable strategy
    """
    
    def __init__(self, pairs, events):
        self.pairs = pairs
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        if event.type == 'TICK' and event.pair == self.pairs[0]:
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(self.pairs[0], "market", "buy", event.time)
                    print event
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(self.pairs[0], "market", "sell", event.time)
                    print event
                    self.events.put(signal)
                    self.invested = False
            self.ticks += 1


