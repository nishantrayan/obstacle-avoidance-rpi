import motor
import sensor
import time
import RPi.GPIO as gpio
print "Starting up car"

try:
    while True:
        motor.move_forward(100)
        angle = sensor.sense_angles()
        print "Sensed obstacle at", angle
        if angle >= 90:
            motor.turn_right(angle - 90)
        else:
            motor.turn_left(angle + 90)
    
except KeyboardInterrupt:
        print "Cleaning up"
        gpio.cleanup()
