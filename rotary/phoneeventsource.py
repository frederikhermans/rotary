from collections import namedtuple

import events
from events import Event
import RPi.GPIO as GPIO

CHANNEL_DIAL_MOVED = 2
CHANNEL_PULSE = 3
CHANNEL_HANGUP = 4

ChannelConfig = namedtuple('ChannelConfig', ('edge', 'callback', 'bouncetime'))


class PhoneEventSource(object):

    def __init__(self, trigger_fn):
        self._pulses = 0
        self._trigger = trigger_fn
        self._init_gpio({
            CHANNEL_DIAL_MOVED: ChannelConfig(GPIO.RISING, self._dial_moved, 200),
            CHANNEL_PULSE: ChannelConfig(GPIO.BOTH, self._pulse, 75),
            CHANNEL_HANGUP: ChannelConfig(GPIO.RISING, self._hangup, 500),
        })

    def _init_gpio(self, channels):
        GPIO.setmode(GPIO.BCM)
        for channel, config in channels.iteritems():
            GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(channel, *config)

    def _dial_moved(self, _):
        if self._pulses > 0:
            digit = str(self._pulses % 10)
            self._trigger(Event(events.DIGIT_DIALED, digit))
        self._pulses = 0

    def _pulse(self, _):
        self._pulses += 1

    def _hangup(self, _):
        self._trigger(Event(events.HANGUP, None))
