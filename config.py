# This file connects buttons to sounds.
# A button is connected to a GPIO pin which has a number.
# The number is the physical pin number, not the Linux GPIO number.
# Define tuples in the array below like this:
# (<physical GPIO pin number>, <filename of sound file in directory 'sounds'>, <what the sound sounds like>)
# The file must be a .wav file.
# An easy way to convert an .mp3 file to .wav:
# ffmpeg -i sounds/leka.mp3 sounds/leka.wav

button_sounds = [
	(10, 'leka.wav', 'Leka'),
	(12, 'pew.wav', 'Pew')
]

# Your dog's name, visible on the web page.

dog_name = 'Ella'
