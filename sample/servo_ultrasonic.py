import RPi.GPIO as gpio
import time
## Upgrading to RPi 3 B model

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)

SERVO_GPIO = 3
ULTRASONIC_ECHO = 5
ULTRASONIC_TRIGGER = 7

gpio.setup(ULTRASONIC_TRIGGER, gpio.OUT)
gpio.output(ULTRASONIC_TRIGGER, False)
gpio.setup(ULTRASONIC_ECHO, gpio.IN)

gpio.setup(SERVO_GPIO, gpio.OUT)
servo_pin = gpio.PWM(SERVO_GPIO, 50)
servo_pin.start(7.5)

def move_sensor_servo(angle):
    pulse_time_ms = 0.5 + ((2.0 * angle) / 180)
    duty_cycle = (pulse_time_ms / 20) * 100
    servo_pin.ChangeDutyCycle(duty_cycle)
    time.sleep(0.05)
    
def detect_distance(angle):
    # Move servo to specific angle
    # Emit ultra sonic wave
    # Return distance after detecting time of echo
    # if wave doesn't return in specific time just return -1
    move_sensor_servo(angle)

    gpio.output(ULTRASONIC_TRIGGER, True)
    time.sleep(0.00001)
    gpio.output(ULTRASONIC_TRIGGER, False)
    start_scan = time.time()
    while gpio.input(ULTRASONIC_ECHO) == 0:
        pass
    
    start = time.time()
    while gpio.input(ULTRASONIC_ECHO) == 1:
        if (time.time() - start_scan) > 0.0014:
            print "Breaking out because it took time"
            break
        pass
    print "Time Taken", (time.time() - start_scan)
    stop = time.time()
    distance_cm = (stop - start) * 17000
    return distance_cm

def detect_obstacle():
    while True:
        min_distance = -1
        min_distance_angle = 0
        for angle in range(0, 181, 10):
           distance = detect_distance(angle)
           print angle, distance
           if(min_distance == -1 or distance < min_distance):
               min_distance = distance
               min_distance_angle = angle
        print "Min", min_distance_angle, min_distance
        move_sensor_servo(min_distance_angle)
        time.sleep(1)

try:
   
    detect_obstacle()        

except KeyboardInterrupt:
    servo_pin.ChangeDutyCycle(7.5)
    print "Resetting to Neutral"
    time.sleep(1)
    servo_pin.stop()
    gpio.cleanup()
