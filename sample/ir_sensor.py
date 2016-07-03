import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.IN)
while True:
    i = gpio.input(12)
    print i
    if i == 0:
        print "Obstacle detected"
    time.sleep(0.1)
