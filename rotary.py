#!/usr/bin/python -u

from __future__ import print_function

import os
import re
import time

import pygame
import RPi.GPIO as GPIO

RE_SOUND_FILE = re.compile(r'^(?P<number>[\d]+)\....$')


class Dialer(object):

    def __init__(self, on_number_dialled, movement_end_channel=2, pulse_channel=3, hangup_channel=4):
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
        self._dialed = ''
        self._on_number_dialled = on_number_dialled

    def _on_movement_end(self, _):
        if self._pulses > 0:
            print(self._pulses % 10, end='')
            self._dialed += str(self._pulses % 10)
            self._on_number_dialled(self._dialed)
        self._pulses = 0

    def _on_pulse(self, _):
        self._pulses += 1

    def _on_hangup(self, _):
        if len(self._dialed):
            print('\r{}\r'.format('_' * len(self._dialed)), end='')
        self._dialed = ''
        # This shouldn't be here, but be part of the player
        pygame.mixer.music.stop()


class Player(object):

    def __init__(self, sound_dir):
        pygame.mixer.init()

        self._sound_files = dict()
        for filename in os.listdir(sound_dir):
            m = RE_SOUND_FILE.match(filename)
            if m and os.path.isfile(sound_dir + '/' + filename):
                number = m.groupdict()['number']
                self._sound_files[number] = sound_dir + '/' + filename

        print('Loaded sound files for the following numbers:',
              ', '.join(self._sound_files.keys()))

    def on_number_dialed(self, dialed):
        for number, filename in self._sound_files.iteritems():
            if dialed.endswith(number):
                print('Playing', number)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()


def main():
    player = Player('sounds/')
    Dialer(player.on_number_dialed)

    print('Press CTRL+C to quit.')
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
