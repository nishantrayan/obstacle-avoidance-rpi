import RPi.GPIO as gpio
import time
# Following Untested in real environment
R_IN1 = 13
R_IN2 = 15
R_ENA1 = 7
R_ENA2 = 11
L_ENA1 = 16
L_ENA2 = 18
L_IN1 = 22
L_IN2 = 24

L_ENA_PINS = []
R_ENA_PINS = []


def move_left_side(speed, dir='forward'):
    gpio.output(L_ENA1, True)
    gpio.output(L_ENA2, True)
    for ena_pin in L_ENA_PINS:
        ena_pin.start(speed)

    if dir == 'forward':
        gpio.output(L_IN1, True)
        gpio.output(L_IN2, False)
    else:
        if dir == 'backward':
            gpio.output(L_IN1, False)
            gpio.output(L_IN2, True)
   
def move_right_side(speed, dir='forward'):
    gpio.output(R_ENA1, True)
    gpio.output(R_ENA2, True)
    if dir == 'forward':
        print "Moving right side forward"
        gpio.output(R_IN1, True)
        gpio.output(R_IN2, False)
    else:
        if dir == 'backward':
            gpio.output(R_IN1, False)
            gpio.output(R_IN2, True)
    for ena_pin in R_ENA_PINS:
        ena_pin.start(speed)

def move_forward(speed):
    stop_left()
    stop_right()
    print "Moving forward"
    move_left_side(speed)
    move_right_side(speed)

def move_backward(speed):
    stop_left()
    stop_right()
    move_left_side(speed, 'backward')
    move_right_side(speed, 'backward')

def stop_left():
    for pin in [L_IN1, L_IN2, L_ENA1, L_ENA2]:
        gpio.output(pin, False)


def stop_right():
    for pin in [R_IN1, R_IN2, R_ENA1, R_ENA2]:
        gpio.output(pin, False)

def turn_left(angle):
    stop_left()
    move_right_side(50)
    time.sleep(2)

def turn_right(angle):
    stop_right()
    move_left_side(50)
    time.sleep(2)

if __name__ != '__motor__':
    print "Initializing motor"
    gpio.setwarnings(False)
    gpio.setmode(gpio.BOARD)

    for out_pin in [L_IN1, L_IN2, L_ENA1, L_ENA2, R_IN1, R_IN2, R_ENA1, R_ENA2]:
        gpio.setup(out_pin, gpio.OUT)

    L_ENA_PINS.append(gpio.PWM(L_ENA1, 100))
    L_ENA_PINS.append(gpio.PWM(L_ENA2, 100))
    R_ENA_PINS.append(gpio.PWM(R_ENA1, 100))
    R_ENA_PINS.append(gpio.PWM(R_ENA2, 100))
