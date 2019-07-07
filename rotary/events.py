from collections import namedtuple

DIGIT_DIALED = 1
CONNECTING = 2
CONNECTED = 3
HANGUP = 4
NO_SERVICE = 5
KEEP_ALIVE = 6

Event = namedtuple('Event', ('type', 'payload'))
