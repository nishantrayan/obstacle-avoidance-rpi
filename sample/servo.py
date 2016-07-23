import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

gpio.setup(3, gpio.OUT)
p = gpio.PWM(3, 50)
p.start(7.5)

try:
    while True:
        p.ChangeDutyCycle(7.5)
        print "Neutral"
        time.sleep(1)
        p.ChangeDutyCycle(12.5)
        print "180"
        time.sleep(1)
        p.ChangeDutyCycle(2.5)
        print "0"
        time.sleep(1)
        

except KeyboardInterrupt:
    p.ChangeDutyCycle(7.5)
    print "Resetting to Neutral"
    time.sleep(1)
    p.stop()
    gpio.cleanup()
