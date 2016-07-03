import RPi.GPIO as gpio
import time
gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

gpio.output(7, True)
gpio.output(11, True)
ena1 = gpio.PWM(7, 100)
ena2 = gpio.PWM(11, 100)
ena1.start(30)
ena2.start(30)
for x in range(0, 1):
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(2)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(2)
    print "Stopping"
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(1)
gpio.output(7, False)
gpio.output(11, False)
