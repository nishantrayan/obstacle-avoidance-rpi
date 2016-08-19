import motor
import sensor
print "Starting up car"

if __name__ == '__init__':
    motor.move_forward(100)
    angle = sensor.sense_angles()
    motor.move_backward()
