#!/usr/bin/python -u

from __future__ import print_function

from collections import namedtuple
import os
import sched
import time

import pygame
import RPi.GPIO as GPIO

MAX_EVENT_DELAY_SECONDS = 0.1
EVENT_DIGIT_DIALED = 1
EVENT_CONNECTING = 2
EVENT_CONNECTED = 3
EVENT_HANGUP = 4
EVENT_NO_SERVICE = 5

Event = namedtuple('Event', ('type', 'payload'))


class PhoneEventSource(object):

    def __init__(self, movement_end_channel=2, pulse_channel=3, hangup_channel=4):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(movement_end_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pulse_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(hangup_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            movement_end_channel, GPIO.RISING, callback=self._on_movement_end, bouncetime=200)
        GPIO.add_event_detect(
            pulse_channel, GPIO.BOTH, callback=self._on_pulse, bouncetime=75)
        GPIO.add_event_detect(
            hangup_channel, GPIO.RISING, callback=self._on_hangup, bouncetime=500)

        self._pulses = 0
        self._schedule_function = None

    def set_schedule_function(self, fn):
        self._schedule_function = fn

    def _on_movement_end(self, _):
        if self._pulses > 0:
            print(self._pulses % 10, end='')
            if self._schedule_function:
                self._schedule_function(
                    0, Event(EVENT_DIGIT_DIALED, str(self._pulses % 10)))
        self._pulses = 0

    def _on_pulse(self, _):
        self._pulses += 1

    def _on_hangup(self, _):
        if self._schedule_function:
            self._schedule_function(0, Event(EVENT_HANGUP, None))


class Player(object):

    def __init__(self, sound_dir):
        pygame.mixer.init()

        self._sound_dir = sound_dir

        assert self.has_sound('ring')
        assert self.has_sound('dial')
        assert self.has_sound('noservice')
        self._ringtone_filename = sound_dir + '/' + 'ring.mp3'
        self._dialtone_filename = sound_dir + '/' + 'dial.mp3'
        self._noservice_filename = sound_dir + '/' + 'noservice.mp3'

    def ringtone(self):
        print('\rRinging', end='')
        self._stop_load_play(self._ringtone_filename)

    def dialtone(self):
        print('\rDialtone', end='')
        self._stop_load_play(self._dialtone_filename, forever=True)

    def play(self, number):
        print('\rPlaying', number, end='')
        self._stop_load_play(self._sound_dir + '/' + number + '.mp3')

    def noservice(self):
        print('\rNo service', end='')
        self._stop_load_play(self._noservice_filename, forever=True)

    def has_sound(self, number):
        return os.path.isfile(self._sound_dir + '/' + number + '.mp3')

    def stop(self):
        pygame.mixer.music.stop()

    def _stop_load_play(self, filename, forever=False):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=-1 if forever else 0)


class Controller(object):

    def __init__(self, player, phone_event_source):
        self._is_idle = True
        self._dialed = ''
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._scheduler.enter(MAX_EVENT_DELAY_SECONDS, 0,
                              self._keepalive, tuple())

        self._player = player
        phone_event_source.set_schedule_function(self.schedule_event)

    def _keepalive(self):
        # This is a fugly hack because our scheduler doesn't wake up if we
        # schedule events from other threads. By scheduling a NOP event
        # every MAX_EVENT_DELAY_SECONDS, we make sure that all events are
        # processed within the given bound. It's super inefficient.
        self._scheduler.enter(MAX_EVENT_DELAY_SECONDS, 0,
                              self._keepalive, tuple())

    def _handle_event(self, event):
        if event.type == EVENT_DIGIT_DIALED:
            if self._is_idle:
                self._player.stop()
                self._dialed += event.payload
                if self._player.has_sound(self._dialed):
                    self._is_idle = False
                    self.schedule_event(
                        0, Event(EVENT_CONNECTING, self._dialed))
                elif len(self._dialed) > 6:
                    self.schedule_event(0, Event(EVENT_NO_SERVICE, None))
        elif event.type == EVENT_CONNECTING:
            self._player.ringtone()
            self.schedule_event(10.5, Event(EVENT_CONNECTED, event.payload))
        elif event.type == EVENT_CONNECTED:
            self._player.play(event.payload)
        elif event.type == EVENT_HANGUP:
            # TODO: Clear pending events
            self._is_idle = True
            self._dialed = ''
            self._player.dialtone()
        elif event.type == EVENT_NO_SERVICE:
            self._player.noservice()

    def run(self):
        self._scheduler.run()

    def schedule_event(self, delay_seconds, evt):
        self._scheduler.enter(delay_seconds, 0, self._handle_event, (evt, ))


def main():
    player = Player('sounds')
    phone_event_source = PhoneEventSource()
    controller = Controller(player, phone_event_source)

    print('Press CTRL+C to quit.')
    try:
        controller.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
