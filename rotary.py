#!/usr/bin/python -u

from __future__ import print_function

import RPi.GPIO as GPIO
import pygame
import time

# Getting warning "RuntimeWarning: A physical pull up resistor is fitted on this channel!" for PIN2.
# * Even though I've specified GPIO.RISING, I'm still sporadically
#   getting callbacks on what I believe should be a falling edge.
# * Bouncetime of 75ms seems to work flawlessly on the pulse detector
# * Would be nicer to use pygame.mixer.Sound() objects, but they cannot be MP3 (need WAV or OGG)

pulses = 0
number = ''

def movement_ended(channel):
    global pulses, number
    if pulses > 0:
        number += str(pulses % 10)
        print(number)
        if number.endswith('235898'):
            print('Playing sound...')
            pygame.mixer.music.play(loops=0, start=53)

    pulses = 0

def pulse(channel):
    global pulses
    pulses += 1

def watch(channel, delay_seconds=0.01):
    while True:
        print(GPIO.input(channel), end='') 
        time.sleep(delay_seconds)

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(2, GPIO.RISING, callback=movement_ended, bouncetime=200)
    GPIO.add_event_detect(3, GPIO.BOTH, callback=pulse, bouncetime=75)

    pygame.mixer.init()
    pygame.mixer.music.load("sounds/final_countdown.mp3")
    pygame.mixer.music.set_volume(1.0)

    print('Press CTRL+C to quit.')
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
