import motor
import sensor
print "Starting up car"

if __name__ == '__init__':
    motor.move_forward(100)
    angle = sensor.sense_angles()
    if angle >= 90:
        motor.turn_right(angle - 90)
    else:
        motor.turn_left(angle + 90)
    motor.move_forward()
