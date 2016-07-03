import RPi.GPIO as gpio
import time

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
##setup variables for pins
IR_LEFT = 12
IR_RIGHT = 26
MOTOR_MOVE_IN1 = 13
MOTOR_MOVE_IN2 = 15
MOTOR_MOVE_ENA1 = 7
MOTOR_MOVE_ENA2 = 11
MOTOR_DIR_ENA1 = 16
MOTOR_DIR_ENA2 = 18
MOTOR_DIR_IN1 = 22
MOTOR_DIR_IN2 = 24

FORWARD_SPEED = 60
BACKWARD_SPEED = 100
IR_PINS = [IR_LEFT, IR_RIGHT]

##setup inputs and outputs
for ir_pin in IR_PINS:
    gpio.setup(ir_pin, gpio.IN)
    
for out_pin in [MOTOR_MOVE_IN1, MOTOR_MOVE_IN2, MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2, MOTOR_DIR_IN1, MOTOR_DIR_IN2, MOTOR_DIR_ENA1, MOTOR_DIR_ENA2]:
    gpio.setup(out_pin, gpio.OUT)
enas = []
for ena_pin in [MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2]:
    enas.append(gpio.PWM(ena_pin, 100))

def detect_obstacle():
    max_confidence = 1
    confidence = max_confidence
    while True:
        detected = False
        for ir_pin in IR_PINS:
            ir_value = gpio.input(ir_pin)
            if ir_value == 0:
                detected = True
            time.sleep(0.1)    
            
        if detected:
            print "Detected"
            print confidence
            confidence = confidence - 1
            if confidence == 0:
                return True
        else:
            print "All clear"
            confidence = max_confidence
        time.sleep(0.1)    
            

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
    time.sleep(0.5)
    for ena_pin in enas:
        ena_pin.start(BACKWARD_SPEED)
    gpio.output(MOTOR_MOVE_IN1, True)
    gpio.output(MOTOR_MOVE_IN2, False)
    
while True:
    forward()    
    detect_obstacle()
    stop()
    time.sleep(0.5)
    backup()
    time.sleep(2)
    stop()
    time.sleep(0.5)
