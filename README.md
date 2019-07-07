# Raspberry Pi-powered Rotary Phone

This is a program that plays sounds based on inputs from a rotary phone. Here's a video where you can [see it in action](https://youtu.be/dZN5T5G_DpY). Crank up your volume.

Killer features:

* carrier tone (dial tone)
* ring tone
* different sounds for different numbers
* no-service message for invalid numbers.

## Quick instructions

* Connect the hook to GPIO pin 4
* Connect the rotary movement indicator to GPIO pin 3
* Connect the pulse indicator to GPIO pin 2
* Create a sounds/ directory with the following files
  * `dial.mp3` should contain the carrier tone (dial tone) ([examples](https://www.soundsnap.com/tags/telephone_tone))
  * `ring.mp3` should contain the ring tone ([examples](https://www.soundsnap.com/tags/telephone_tone))
  * `noservice.mp3` should contain the sound to be played on no service ([example](https://www.youtube.com/watch?v=rKFAA-ntKXg))
  * `$NUMBER.mp3` will be played if $NUMBER is dialed on the rotary dial. Eg, `231344.mp3` will be played if you dial 231344.
* Attach a USB sound dongle to your Raspberry Pi, and connect it to the earpiece's speaker. I simply attached a 3.5mm plug to the cable coming from the earpiece.
* Run it: `$ python rotary/main.py`

## Bugs and issues

* Dialtone plays even though the earpiece is on the hook
* Hanging up while ringing will not cancel playing the scheduled sound
