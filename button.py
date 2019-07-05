#!/usr/bin/python

from __future__ import print_function

import RPi.GPIO as GPIO
import time

# Getting warning "RuntimeWarning: A physical pull up resistor is fitted on this channel!" for PIN2.

def callback(channel):
    print('Got a callback from channel', channel)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(2, GPIO.BOTH, callback=callback, bouncetime=200)

    print('Press CTRL+C to quit.')
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
