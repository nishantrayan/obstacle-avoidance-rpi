import RPi.GPIO as gpio
import time
import math
## Upgrading to RPi 3 B model

VIBRATION_PIN = 8
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(VIBRATION_PIN, gpio.IN, pull_up_down=gpio.PUD_DOWN)


def move_callback(pin):
    print "Moved! on", pin

gpio.add_event_detect(VIBRATION_PIN, gpio.RISING, callback=move_callback, bouncetime=1)

try:
    while True:
        pass
except KeyboardInterrupt:
    gpio.cleanup()
