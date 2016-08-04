import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
##setup variables for pins
VIBRATION_PIN = 10
ULTRASONIC_TRIG = 26
ULTRASONIC_ECHO = 29
SERVO_GPIO = 12

MOTOR_MOVE_IN1 = 15
MOTOR_MOVE_IN2 = 13
MOTOR_MOVE_ENA1 = 7
MOTOR_MOVE_ENA2 = 11
MOTOR_DIR_ENA1 = 16
MOTOR_DIR_ENA2 = 18
MOTOR_DIR_IN1 = 22
MOTOR_DIR_IN2 = 24

FORWARD_SPEED = 85
BACKWARD_SPEED = 100
OBSTACLE_DISTANCE_CM = 20
SPEED_CHECK_INTERVAL_SEC = 2.0
MIN_ANGLE = 35
MAX_ANGLE = 145
STEP_ANGLE = 10
for out_pin in [MOTOR_MOVE_IN1, MOTOR_MOVE_IN2, MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2, MOTOR_DIR_IN1, MOTOR_DIR_IN2, MOTOR_DIR_ENA1, MOTOR_DIR_ENA2]:
    gpio.setup(out_pin, gpio.OUT)

gpio.setup(VIBRATION_PIN, gpio.IN, pull_up_down=gpio.PUD_DOWN)

gpio.setup(ULTRASONIC_TRIG, gpio.OUT)
gpio.output(ULTRASONIC_TRIG, False)
gpio.setup(ULTRASONIC_ECHO, gpio.IN)

gpio.setup(SERVO_GPIO, gpio.OUT)
servo_pin = gpio.PWM(SERVO_GPIO, 50)
servo_pin.start(7.5)

enas = []
for ena_pin in [MOTOR_MOVE_ENA1, MOTOR_MOVE_ENA2]:
    enas.append(gpio.PWM(ena_pin, 100))

moved = False
move_check_time = time.time()
def moved(vibration_pin):
    global moved
    moved = True
   
def stuck():
    global moved
    global move_check_time
    has_moved = moved
    current_time = time.time()
    if(current_time - move_check_time) > SPEED_CHECK_INTERVAL_SEC:
        if not(has_moved):
            print "Stuck", current_time
        moved = False
        move_check_time = current_time
        return not(has_moved)
    return False

gpio.add_event_detect(VIBRATION_PIN, gpio.RISING, callback=moved, bouncetime=1)

def obstacle_detected():
    for angle in range(MIN_ANGLE, MAX_ANGLE, STEP_ANGLE):
        move_sensor_servo(angle)
        distance = detect_distance()
        if distance <= OBSTACLE_DISTANCE_CM:
            move_sensor_servo(angle)
            print "Object detected", angle, distance
            return True
    return False
           
def move_sensor_servo(angle):
    pulse_time_ms = 0.5 + ((2.0 * angle) / 180)
    duty_cycle = (pulse_time_ms / 20) * 100
    servo_pin.ChangeDutyCycle(duty_cycle)
    time.sleep(0.075)
    
def detect_distance():
    gpio.output(ULTRASONIC_TRIG, True)
    time.sleep(0.00001)
    gpio.output(ULTRASONIC_TRIG, False)
    start_scan = time.time()
    while gpio.input(ULTRASONIC_ECHO) == 0:
        pass
    
    start = time.time()
    while gpio.input(ULTRASONIC_ECHO) == 1:
        pass
    stop = time.time()
    distance_cm = (stop - start) * 17000
    return distance_cm
            

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
    time.sleep(0.25)
    for ena_pin in enas:
        ena_pin.start(BACKWARD_SPEED)
    gpio.output(MOTOR_MOVE_IN1, True)
    gpio.output(MOTOR_MOVE_IN2, False)

try:
    forward()
    while True:
        if stuck() or obstacle_detected():
            stop()
            time.sleep(0.25)
            backup()
            time.sleep(1)
            stop()
            time.sleep(0.25)
            forward()
        
except KeyboardInterrupt:
        print "Cleaning up"
        gpio.cleanup()
