import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
##setup variables for pins
ULTRASONIC_TRIG_MID = 26
ULTRASONIC_ECHO_MID = 29
ULTRASONIC_TRIG_RIGHT = 31
ULTRASONIC_ECHO_RIGHT = 32
ULTRASONIC_TRIG_LEFT = 33
ULTRASONIC_ECHO_LEFT = 35


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
OBSTACLE_DISTANCE_CM = 20
for out_pin in [MOTOR_MOVE_IN1, MOTOR_MOVE_IN2, MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2, MOTOR_DIR_IN1, MOTOR_DIR_IN2, MOTOR_DIR_ENA1, MOTOR_DIR_ENA2]:
    gpio.setup(out_pin, gpio.OUT)

ULTRASONIC_TRIG_PINS = [ULTRASONIC_TRIG_LEFT, ULTRASONIC_TRIG_RIGHT, ULTRASONIC_TRIG_MID]
ULTRASONIC_ECHO_PINS = [ULTRASONIC_ECHO_LEFT, ULTRASONIC_ECHO_RIGHT, ULTRASONIC_ECHO_MID]
for trig_pin in ULTRASONIC_TRIG_PINS:
    gpio.setup(trig_pin, gpio.OUT)
    gpio.output(trig_pin, False)

for echo_pin in ULTRASONIC_ECHO_PINS:    
    gpio.setup(echo_pin, gpio.IN)

enas = []
for ena_pin in [MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2]:
    enas.append(gpio.PWM(ena_pin, 100))



def detect_obstacle():
    while True:
        for idx, trig_pin in enumerate(ULTRASONIC_TRIG_PINS):
            echo_pin = ULTRASONIC_ECHO_PINS[idx]
            time.sleep(0.1)
            gpio.output(trig_pin, True)
            time.sleep(0.00001)
            gpio.output(trig_pin, False)
            while gpio.input(echo_pin) == 0:
                pass
            start = time.time()
            while gpio.input(echo_pin) == 1:
                pass
            stop = time.time()
            distance_cm = (stop - start) * 17000
            if distance_cm <= OBSTACLE_DISTANCE_CM:
                print "Object detected by", idx, "at", time.time()
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
