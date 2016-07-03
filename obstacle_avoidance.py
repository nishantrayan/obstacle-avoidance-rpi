import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
##setup variables for pins
IR_LEFT = 12
MOTOR_MOVE_IN1 = 13
MOTOR_MOVE_IN2 = 15
MOTOR_MOVE_ENA1 = 7
MOTOR_MOVE_ENA2 = 11
##setup inputs and outputs
gpio.setup(IR_LEFT, gpio.IN)
for out_pin in [MOTOR_MOVE_IN1, MOTOR_MOVE_IN2, MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2]:
    gpio.setup(out_pin, gpio.OUT)
gpio.output(MOTOR_MOVE_ENA1, True)
gpio.output(MOTOR_MOVE_ENA2, True)
ena1 = gpio.PWM(MOTOR_MOVE_ENA1, 100)
ena2 = gpio.PWM(MOTOR_MOVE_ENA2, 100)
ena1.start(30)
ena2.start(30)


def forward():
    gpio.output(MOTOR_MOVE_IN1, False)
    gpio.output(MOTOR_MOVE_IN2, True)    

def stop():
    gpio.output(MOTOR_MOVE_IN1, False)
    gpio.output(MOTOR_MOVE_IN2, False)
    
for x in range(0, 1):
    forward()
    time.sleep(2)
    stop()
    time.sleep(1)
gpio.output(MOTOR_MOVE_ENA1, False)
gpio.output(MOTOR_MOVE_ENA2, False)
