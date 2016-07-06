import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
##setup variables for pins
ULTRASONIC_TRIG = 26
ULTRASONIC_ECHO = 29

MOTOR_MOVE_IN1 = 15
MOTOR_MOVE_IN2 = 13
MOTOR_MOVE_ENA1 = 7
MOTOR_MOVE_ENA2 = 11
MOTOR_DIR_ENA1 = 16
MOTOR_DIR_ENA2 = 18
MOTOR_DIR_IN1 = 22
MOTOR_DIR_IN2 = 24

FORWARD_SPEED = 75
BACKWARD_SPEED = 100
OBSTACLE_DISTANCE_CM = 15
for out_pin in [MOTOR_MOVE_IN1, MOTOR_MOVE_IN2, MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2, MOTOR_DIR_IN1, MOTOR_DIR_IN2, MOTOR_DIR_ENA1, MOTOR_DIR_ENA2]:
    gpio.setup(out_pin, gpio.OUT)
    
gpio.setup(ULTRASONIC_TRIG, gpio.OUT)
gpio.output(ULTRASONIC_TRIG, False)
gpio.setup(ULTRASONIC_ECHO, gpio.IN)

enas = []
for ena_pin in [MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2]:
    enas.append(gpio.PWM(ena_pin, 100))



def detect_obstacle():
    while True:
        time.sleep(0.1)
        gpio.output(ULTRASONIC_TRIG, True)
        time.sleep(0.00001)
        gpio.output(ULTRASONIC_TRIG, False)
        while gpio.input(ULTRASONIC_ECHO) == 0:
            pass
        start = time.time()
        while gpio.input(ULTRASONIC_ECHO) == 1:
            pass
        stop = time.time()
        distance_cm = (stop - start) * 17000
        if distance_cm <= OBSTACLE_DISTANCE_CM:
            print "Object detected", time.time()
            return
            

def forward():
    gpio.output(MOTOR_DIR_ENA1, True)
    gpio.output(MOTOR_DIR_ENA2, True)
    gpio.output(MOTOR_MOVE_ENA1, True)
    gpio.output(MOTOR_MOVE_ENA2, True)
    gpio.output(MOTOR_DIR_IN1, False)
    gpio.output(MOTOR_DIR_IN2, False)
    for ena_pin in enas:
        ena_pin.start(FORWARD_SPEED)
    time.sleep(0.5)    
    gpio.output(MOTOR_MOVE_IN1, False)
    gpio.output(MOTOR_MOVE_IN2, True)    

def stop():
    gpio.output(MOTOR_MOVE_ENA1, False)
    gpio.output(MOTOR_MOVE_ENA2, False)
    gpio.output(MOTOR_DIR_ENA1, False)
    gpio.output(MOTOR_DIR_ENA2, False)
    gpio.output(MOTOR_MOVE_IN1, False)
    gpio.output(MOTOR_MOVE_IN2, False)
    gpio.output(MOTOR_DIR_IN1, False)
    gpio.output(MOTOR_DIR_IN2, False)

def backup():
    gpio.output(MOTOR_DIR_ENA1, True)
    gpio.output(MOTOR_DIR_ENA2, True)
    gpio.output(MOTOR_MOVE_ENA1, True)
    gpio.output(MOTOR_MOVE_ENA2, True)
    gpio.output(MOTOR_DIR_IN1, True)
    gpio.output(MOTOR_DIR_IN2, False)
    time.sleep(1)
    for ena_pin in enas:
        ena_pin.start(BACKWARD_SPEED)
    gpio.output(MOTOR_MOVE_IN1, True)
    gpio.output(MOTOR_MOVE_IN2, False)

try:    
    while True:
        forward()    
        detect_obstacle()
        stop()
        time.sleep(0.5)
        backup()
        time.sleep(2)
        stop()
        time.sleep(0.5)
except KeyboardInterrupt:
        print "Cleaning up"
        gpio.cleanup()
