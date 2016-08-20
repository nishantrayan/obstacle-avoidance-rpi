import motor
import sensor
import time
import RPi.GPIO as gpio
print "Starting up car"

motor.move_forward(100)
time.sleep(2)
motor.stop_left()
motor.stop_right()
motor.turn_right(10)
time.sleep(2)
gpio.cleanup()
    #angle = sensor.sense_angles()
    #if angle >= 90:
    #    motor.turn_right(angle - 90)
    #else:
    #    motor.turn_left(angle + 90)
    #motor.move_forward()
