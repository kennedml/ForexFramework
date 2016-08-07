#Parent Class
class Event(object):
    pass


# Event Child Class
class TickEvent(Event):
    def __init__(self, pair, time, candleOpen, candleClose, candleHigh, candleLow):
        self.type = 'TICK'
        self.pair = pair
        self.time = time
        self.candleOpen = candleOpen
        self.candleClose = candleClose
        self.candleHigh = candleHigh
        self.candleLow = candleLow

    def __str__(self):
        return "Type: %s, Pair: %s, Time: %s, Open: %s, Close: %s, High: %s, Low: %s" % (
            str(self.type), str(self.pair), 
            str(self.time), str(self.candleOpen), str(self.candleClose),
            str(self.candleHigh), str(self.candleLow)
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

