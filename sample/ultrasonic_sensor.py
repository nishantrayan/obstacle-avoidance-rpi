import RPi.GPIO as gpio
import time

## Ultra sonic sensor
gpio.setmode(gpio.BOARD)
TRIG = 31
ECHO = 32

gpio.setup(TRIG, gpio.OUT)
gpio.output(TRIG, False)

gpio.setup(ECHO, gpio.IN)
time.sleep(0.1)
print "Starting measurement"

while True:
  time.sleep(1)
  gpio.output(TRIG, True)
  time.sleep(0.00001)
  gpio.output(TRIG, False)
  while gpio.input(ECHO) == 0:
    pass
  start = time.time()
  while gpio.input(ECHO) == 1:
    pass
  stop = time.time()
  print (stop - start) * 170000

gpio.cleanup()
