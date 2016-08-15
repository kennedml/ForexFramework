#Parent Class
class Event(object):
    pass


# Event Child Class
class TickEvent(Event):
    def __init__(self, pair, time, askOpen, askClose, askHigh, askLow, bidOpen, bidClose, bidHigh, bidLow):
        self.type = 'TICK'
        self.pair = pair
        self.time = time
        self.askOpen = askOpen
        self.askClose = askClose
        self.askHigh = askHigh
        self.askLow = askLow
        self.bidOpen = bidOpen
        self.bidClose = bidClose
        self.bidHigh = bidHigh
        self.bidLow = bidLow

    def __str__(self):
        return "Type: %s, Pair: %s, Time: %s, askOpen: %s, askClose: %s,askHigh: %s, askLow: %s bidOpen: %s, bidClose: %s, bidHigh: %s, bidLow: %s" % (
            str(self.type), str(self.pair), 
            str(self.time), str(self.askOpen), str(self.askClose),
            str(self.askHigh), str(self.askLow), str(self.bidOpen),
            str(self.bidClose), str(self.bidHigh), str(self.bidLow)
        )

    def __repr__(self):
        return str(self)


# Event Child Class
class SignalEvent(Event):
    def __init__(self, pair, order_type, side, time):
        self.type = 'SIGNAL'
        self.pair = pair
        self.order_type = order_type
        self.side = side
        self.time = time  # Time of the last tick that generated the signal

    def __str__(self):
        return "Type: %s, Pair: %s, Order Type: %s, Side: %s" % (
            str(self.type), str(self.pair), 
            str(self.order_type), str(self.side)
        )

    def __repr__(self):
        return str(self)

class OrderEvent(Event):
    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side

    def __str__(self):
        return "Type: %s, Instrument: %s, Units: %s, Order Type: %s, Side: %s" % (
            str(self.type), str(self.instrument), str(self.units),
            str(self.order_type), str(self.side)
        )

    def __repr__(self):
        return str(self)
