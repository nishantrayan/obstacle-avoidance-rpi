import RPi.GPIO as gpio
import time

DEFAULT_SENSE_ANGLES = {}
DEFAULT_SENSE_DISTANCE = 10  # in CM
MIN_ANGLE = 0
MAX_ANGLE = 180
STEP_ANGLE = 1

ULTRASONIC_TRIG = 26
ULTRASONIC_ECHO = 29
SERVO_PIN = 12
SERVO_PWM = 0

for angle in range(MIN_ANGLE, MAX_ANGLE, STEP_ANGLE):
    DEFAULT_SENSE_ANGLES[angle] = DEFAULT_SENSE_DISTANCE


def read_current_distance():
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
    return distance_cm


def move_sensor(angle):
    pulse_time_ms = 0.5 + ((2.0 * angle) / 180)
    duty_cycle = (pulse_time_ms / 20) * 100
    SERVO_PWM.ChangeDutyCycle(duty_cycle)
    time.sleep(0.075)

def sense_angles(angle_distances=DEFAULT_SENSE_ANGLES):
    while True:
        for angle, sense_distance in angle_distances.iteritems():
            move_sensor(angle)
            distance = read_current_distance()
            if distance <= sense_distance:
                return angle

if __name__ != '__sensor__':
    print "Initializing sensor"
    gpio.setup(ULTRASONIC_TRIG, gpio.OUT)
    gpio.output(ULTRASONIC_TRIG, False)
    gpio.setup(ULTRASONIC_ECHO, gpio.IN)

    gpio.setup(SERVO_PIN, gpio.OUT)
    SERVO_PWM = gpio.PWM(SERVO_PIN, 50)
    SERVO_PWM.start(7.5)
