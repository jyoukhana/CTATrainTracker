import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)

old_input_state = True
button = True

while True:
    input_state = GPIO.input(18)
    if input_state == False and old_input_state == True:
        buttonStatus = not button
    old_input_state = input_state
