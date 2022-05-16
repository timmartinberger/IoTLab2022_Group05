from servo_ctrl import Motor, Steering

def enter_to_continue():
    while True:
        enter = raw_input("press enter to continue")
        if enter == "":
            return
def test_motor():

    motor = Motor(1)
    velocities = [0, -12.3, 0.9, 10.5, -7.4]

    print "testing the motor"
    
    for velocity in velocities:
        print "set speed to: ", velocity

        pwm = motor.set_speed(velocity)
        print "got ", pwm, " as pwm"
        enter_to_continue()

def test_steering():
    steering = Steering(1)
    angles = [-3, 18, 51.7, 0, -44.2]

    print "testing the steering"

    for angle in angles:
        print "set angle to: ", angle

        pwm = steering.set_angle(angle)
        print "got ", pwm, " as pwm"
        enter_to_continue()

if __name__ == "__main__":
    test_motor()
    enter_to_continue()
    test_steering()