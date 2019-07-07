import sched
import time

from events import Event
import events

MAX_EVENT_DELAY_SECONDS = 0.1


class Controller(object):

    def __init__(self, player):
        self._player = player
        self._is_idle = True
        self._dialed = ''
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._event_handlers = {
            events.DIGIT_DIALED: self._digit_dialed,
            events.CONNECTED: self._connected,
            events.CONNECTING: self._connecting,
            events.HANGUP: self._hangup,
            events.NO_SERVICE: self._no_service,
            events.KEEP_ALIVE: self._keep_alive,
        }

    def run(self):
        self.trigger(Event(events.KEEP_ALIVE, None))
        self._scheduler.run()

    def trigger(self, event, delay_seconds=0.0):
        handler = self._event_handlers[event.type]
        self._scheduler.enter(delay_seconds, 0, handler, (event, ))

    def _digit_dialed(self, event):
        if not self._is_idle:
            return

        self._player.stop()
        self._dialed += event.payload
        if self._player.has_sound(self._dialed):
            self._is_idle = False
            self.trigger(Event(events.CONNECTING, self._dialed))
        elif len(self._dialed) >= 6:
            self.trigger(Event(events.NO_SERVICE, None))
    
    def _connecting(self, event):
        self._player.ringtone()
        self.trigger(Event(events.CONNECTED, event.payload),
                     delay_seconds=10.5)

    def _connected(self, event):
        self._player.play(event.payload)

    def _hangup(self, _):
        # TODO: Clear pending events
        self._is_idle = True
        self._dialed = ''
        self._player.dialtone()

    def _no_service(self, _):
        self._player.noservice()

    def _keep_alive(self, _):
        # This is a fugly hack. The scheduler doesn't wake up if we
        # schedule events from other threads. By scheduling a KEEP_ALIVE
        # every MAX_EVENTS_DELAY_SECONDS, we make sure that all events are
        # processed within the given bound. It's super inefficient.
        self.trigger(Event(events.KEEP_ALIVE, None),
                     delay_seconds=MAX_EVENT_DELAY_SECONDS)
