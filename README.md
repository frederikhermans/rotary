# Raspberry Pi-powered Rotary Phone

This is a program that plays sounds based on inputs from a rotary phone. Here's a video where you can [see it in action](https://youtu.be/dZN5T5G_DpY). Crank up your volume.

## Photos

Here's what the phone looks like on the inside. I'm using a Raspberry Pi Zero. The USB sound dongle is hidden behind the rotary dial.

![Inside of the phone](photos/inside.jpg?raw=true)

The mechanism of the rotary dial is surprisingly simple. Took a while to find a good debouncing value for the GPIO input attached to the pulse indicator, but now it works very reliably.

![Rotary dial mechanism](photos/dial.jpg?raw=true)

Figuring out how to get a signal for whether the phone's on the hook or not also involved some trial and error. It's hard to see in the picture, but the points the yellow and black jumper cables from the Pi go to the hook indicator.

![Hook signal](photos/hook.jpg?raw=true)

## Quick instructions

* Connect the hook to GPIO pin 4
* Connect the rotary movement indicator to GPIO pin 3
* Connect the pulse indicator to GPIO pin 2
* Create a `sounds/` directory with the following files
  * `dial.mp3` should contain the carrier tone (dial tone) ([examples](https://www.soundsnap.com/tags/telephone_tone))
  * `ring.mp3` should contain the ring tone ([examples](https://www.soundsnap.com/tags/telephone_tone))
  * `noservice.mp3` should contain the sound to be played on no service ([example](https://www.youtube.com/watch?v=rKFAA-ntKXg))
  * `$NUMBER.mp3` will be played if $NUMBER is dialed on the rotary dial. Eg, `231344.mp3` will be played if you dial 231344.
* Attach a USB sound dongle to your Raspberry Pi, and connect it to the earpiece's speaker. I simply attached a 3.5mm plug to the cable coming from the earpiece.
* Run it: `$ ./rotary.pi`

## Bugs and issues

* Dialtone plays even though the earpiece is on the hook
* Hanging up while ringing will not cancel playing the scheduled sound
* Edge detection doesn't properly work.
