#!/usr/bin/python3

import RPi.GPIO as GPIO
from threading import Timer
from time import sleep
from enum import Enum
import pygame
import datetime

import config

DELAY = 0.02

class DogButton:
	def __init__(self, pin, soundfile, text):
		self.pin = pin
		self.soundfile = 'sounds/'+soundfile
		self.sound = pygame.mixer.Sound(self.soundfile)
		self.text = text

# States for the push button state machine. Four states are needed because of debouncing.
                
class State(Enum):
	Off = 0
	On = 1
	PerhapsOn = 2
	PerhapsOff = 3

class TalkingDog:
	buttons = []

	def __enter__(self):
		GPIO.setwarnings(False)

		# Use physical pin numbering.
		GPIO.setmode(GPIO.BOARD)

		# Initialize pygame. Needed to call before any Sound objects are created (which happens when 
		# a DogButton object is created).
		pygame.init()

		# Load the pin <-> sound mapping.
		for bs in config.button_sounds:
			self.buttons.append(DogButton(bs[0], bs[1], bs[2]))

		for button in self.buttons:
			# Set the pin to be an input and set initial value to be pulled low (off).
			GPIO.setup(button.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

			# Setup rise/fall events on the pin.
			GPIO.add_event_detect(button.pin, GPIO.BOTH, callback=self.button_callback)

		# Set small buffer for low playback latency.
		pygame.mixer.pre_init(44100, -16, 2, 512)
		pygame.mixer.init(44100, -16, 2, 512)

		self.n_button_presses = 0
		self.state = State.Off

                # Log file for this application.
		self.log_file = open("talkingdog.log","w")
		self.log_file.write(f"Started.\n")

                # The button press list.
		self.html_file = open("presses.html","a")

	def __exit__(self, type, value, tb):
		GPIO.cleanup()
		self.log_file.close()
		self.html_file.close()


	# Find the button object for a specified pin.

	def find_button(self, pin):
		return [button for button in self.buttons if button.pin == pin][0]


	# Called when there is a rising or falling edge on a button input.
        # For a rising/falling edge to be judged as a real button press/release it has to
        # be up/down for at least DELAY seconds.

	def button_callback(self, pin):
		if self.state == State.Off:
			if self.button_state_on(pin):
				self.timer = Timer(DELAY, self.timer_callback, [pin])
				self.timer.start()
				self.state = State.PerhapsOn
		elif self.state == State.On:
			if not self.button_state_on(pin):
				self.timer = Timer(DELAY, self.timer_callback, [pin])
				self.timer.start()
				self.state = State.PerhapsOff
		elif self.state == State.PerhapsOn:
			if not self.button_state_on(pin):
				self.timer.cancel()
				self.state = State.Off
		elif self.state == State.PerhapsOff:
			if self.button_state_on(pin):
				self.timer.cancel()
				self.state = State.On
		else:
			self.log_file.write('ERROR: Unknown state!')


	# Called when the timer times out.
	
	def  timer_callback(self, pin):
		if self.state == State.PerhapsOn:
			self.state = State.On
			self.n_button_presses += 1
			self.button_pressed(pin)
		elif self.state == State.PerhapsOff:
			self.state = State.Off
		else:
			self.log_file.write('ERROR! Timeout should not occur in state '+self.state+'.')


	# Returns the current hardware state of a button.

	def button_state_on(self, pin):
		return GPIO.input(pin)


	# When a button is determined to be pressed, this is called.
	
	def button_pressed(self, pin):
		self.log_file.write(f'<<< {self.n_button_presses} BUTTON {pin} PRESSED >>>')
		button = self.find_button(pin)
		button.sound.play()

		timestamp = datetime.datetime.now().replace(microsecond=0).isoformat(' ')

		self.log_file.write(f"{timestamp} Played {button.soundfile}: {button.text}\n")
		self.log_file.flush()

		self.html_file.write(f'<tr><td class="timestamp-td">{timestamp}</td><td class="text-td">{button.text}</td></tr>\n')
		self.html_file.flush()
	
with TalkingDog() as talking_dog:
	while True:
		sleep(60)
