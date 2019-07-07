import os

import pygame


class Player(object):

    def __init__(self, sound_dir):
        pygame.mixer.init()
        self._sound_dir = sound_dir
        for sound in ('ring', 'dial', 'noservice'):
            if not self.has_sound(sound):
                raise ValueError(
                    'Could not find required sound ' + self._filename(sound))

    def ringtone(self):
        self._stop_load_play(self._filename('ring'))

    def dialtone(self):
        self._stop_load_play(self._filename('dial'), forever=True)

    def play(self, number):
        self._stop_load_play(self._filename(number))

    def noservice(self):
        self._stop_load_play(self._filename('noservice'), forever=True)

    def has_sound(self, sound):
        return os.path.isfile(self._filename(sound))

    def stop(self):
        pygame.mixer.music.stop()

    def _filename(self, sound):
        return self._sound_dir + '/' + sound + '.mp3'

    def _stop_load_play(self, filename, forever=False):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops=-1 if forever else 0)
