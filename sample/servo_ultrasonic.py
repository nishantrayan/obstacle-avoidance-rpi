import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

SERVO_GPIO = 3
gpio.setup(SERVO_GPIO, gpio.OUT)
servo_pin = gpio.PWM(SERVO_GPIO, 50)
servo_pin.start(7.5)

def detect_distance(angle):
    # Move servo to specific angle
    # Emit ultra sonic wave
    # Return distance after detecting time of echo
    # if wave doesn't return in specific time just return -1
    pulse_time_ms = 0.5 + ((2.0 * angle) / 180)
    duty_cycle = (pulse_time_ms / 20) * 100
    servo_pin.ChangeDutyCycle(duty_cycle)
    time.sleep(0.05)
    return 1.0

def detect_obstacle():
    while True:
        for angle in range(0, 181, 10):
           print angle, detect_distance(angle)
##   while True:
##        p.ChangeDutyCycle(7.5)
##        print "Neutral"
##        time.sleep(0.5)
##        p.ChangeDutyCycle(12.5)
##        print "180"
##        time.sleep(0.5)
##        p.ChangeDutyCycle(2.5)
##        print "0"
##        time.sleep(0.5)
##        p.ChangeDutyCycle(3.75)
##        print "45"
##        time.sleep(0.5)  

try:
   
    detect_obstacle()        

except KeyboardInterrupt:
    servo_pin.ChangeDutyCycle(7.5)
    print "Resetting to Neutral"
    time.sleep(1)
    servo_pin.stop()
    gpio.cleanup()
