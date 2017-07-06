# ENGG1000 Robot Rescue 2017
# By 'Salty Robot'

# Terry Agapitos (z5162173)
# Lachlan Chow (z5164192)
# Lucas Way (z5164204)
# Arthur Ching (z5162176)
# Diana (Susan) Huang (z5163931)
# Renée Lu (z5160268)

# Implements the right-hand rule, with some random elements
# as explained in the Rescue Report.

from ev3dev.ev3 import *
from time import sleep, time
import random

rightMotor = LargeMotor(OUTPUT_D)
leftMotor = LargeMotor(OUTPUT_A)
clawMotor = Motor(OUTPUT_B)

usFront = UltrasonicSensor(INPUT_2)
usRight = UltrasonicSensor(INPUT_3)
cs = ColorSensor(INPUT_4)
gs = GyroSensor()
gs.mode = 'GYRO-ANG'

RIGHT_WALL_DIST = 400
FRONT_WALL_DIST = 250

def reset_gyro():
    """
    Resets the gyroscope's value back to 0.
    By changing the mode of the gyroscope, the values reset back to 0.
    """
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

def is_connected():
    """
    Checks that all motors and sensors are connected.
    Returns True if all ports are connected - False otherwise.
    """
    for connection in (rightMotor, leftMotor, clawMotor, usFront, usRight, cs, gs):
        if not connection.connected:
            print("{} is not connected.".format(connection))
            return False
    return True

def release_claw():
    """
    Releases the claw's grasp to allow the can to be free.
    Used mainly for testing purposes when needed to 
    reset the claw back to the beginning.
    """
    clawMotor.run_direct(duty_cycle_sp=30)
    sleep(3)
    clawMotor.stop()

def stop_motors():
    """
    Stops both large motors and allows the robot to cease movement.
    """
    leftMotor.stop()
    rightMotor.stop()
    sleep(0.1)

def turn_left():
    """
    Turns the robot 90 degrees left.
    """
    reset_gyro()
    while gs.value() > -90:
        leftMotor.run_direct(duty_cycle_sp=-30)
        rightMotor.run_direct(duty_cycle_sp=30)
    stop_motors()
    while gs.value() < -90: # If the robot goes past 90 degrees, we correct it back.
        leftMotor.run_direct(duty_cycle_sp=25)
        rightMotor.run_direct(duty_cycle_sp=-25)
    stop_motors()
    reset_gyro()

def turn_180(start):
    """
    Turns the robot in a southern direction. Used when the can has been grabbed.
    It takes one argument, start, which is the angle at which the can is found.
    """
    reset_gyro()
    while gs.value() > -180+start:
        leftMotor.run_direct(duty_cycle_sp=-30)
        rightMotor.run_direct(duty_cycle_sp=30)
    stop_motors()
    while gs.value() < -180+start: # it went over
        leftMotor.run_direct(duty_cycle_sp=25)
        rightMotor.run_direct(duty_cycle_sp=-25)
    stop_motors()
    reset_gyro()


def turn_right():
    """
    Turns the robot 90 degrees right.
    """
    reset_gyro()
    while gs.value() < 90:
        leftMotor.run_direct(duty_cycle_sp=30)
        rightMotor.run_direct(duty_cycle_sp=-30)
    stop_motors()
    while gs.value() > 90: # If the robot goes past 90 degrees, we correct it back.
        leftMotor.run_direct(duty_cycle_sp=-25)
        rightMotor.run_direct(duty_cycle_sp=25)
    stop_motors()
    reset_gyro()
    initTime = time()
    speedA = speedB = 50
    while detect()[1] > RIGHT_WALL_DIST: # While there's emptiness to our right.
        speedA, speedB = balance_gyro(speedA, speedB)
        drive(speedA, speedB) # Drive forward, while still course-correcting.
        if detect()[1] <= RIGHT_WALL_DIST or time() - initTime >= 2:
            # If there's a wall to our right OR we've driven for 2 seconds.
            break
        if detect()[0] < 100:
            # If we're about to hit a wall.
            break
    reset_gyro()

def grab():
    """
    Grabs the claw in front of us.
    """
    clawMotor.run_direct(duty_cycle_sp=-100)
    sleep(1.5) # Give it some time to grab the can.
    clawMotor.duty_cycle_sp = -30 # Still give it some pressure so the can doesn't fall out of grasp.

def detect():
    """
    Returns the values (distances) of both Ultrasonic Sensors as a tuple.

    The front Ultrasonic Sensor is the ev2 model (not ev3).
    Instead of returning the distance in millimetres, it returns it in centimetres.
    Thus, we multiply the result by 10.
    """
    return usFront.value()*10, usRight.value()

def drive(speedX, speedY):
    """
    Drives the robot forward with a given speed.
    """
    leftMotor.run_direct(duty_cycle_sp=speedX)
    rightMotor.run_direct(duty_cycle_sp=speedY)

L = [] # Used for balance()
def balance(speedX, speedY):
    """
    Course corrects the robot when traversing the maze.

    It measures the distance between the robot and the right wall.
    If the distance is decreasing, then we're moving closer to the wall.
    Thus, we speed the right motor up and decrease the left motor to move
    away from the wall.

    If the distance is increasing, then we're moving away from the wall.
    Thus, we speed the left motor up and decrease the right motor.

    Returns the new speeds.
    """
    global L
    L.append(detect()[1]) # Appends the values of the right USS to a list.
    if len(L) == 3: # Once we've read three values.
        res = L[2] - L[0] # The difference of the distances.
        if res < 0: # The distance is decreasing... we're drifting right closer towards the wall
            speedX = 48
            speedY = 51
        elif res > 0: # The distance is increasing... we're drifting left away from the wall
            speedX = 54
            speedY = 46
        L = [] # Reset the list back to an empty list.
    return speedX, speedY

def balance_gyro(speedX, speedY):
    """
    Course corrects the robot when traversing the maze using the gyroscope.

    We use this one - as opposed to the other balance function - when
    there is no wall to the right of us.
    """
    if gs.value() >= 1: # It's drifting right, so go left.
        speedY = 54 # Speed up the right motor.
        speedX = 46 # SLow down the left motor.
    elif gs.value() < 1: # It's drifting left, so go right.
        speedX = 51
        speedY = 49
    else: # It's all good
        speedX = speedY = 50
    reset_gyro()
    return speedX, speedY

def kick():
    """
    'Kicks' the robot forward a little.
    """
    initTime = time()
    while time()-initTime < 0.1: # Drive forward a little bit
       speedX, speedY = balance_gyro(speedX, speedY)
       drive(speedX, speedY)
    stop_motors()

def main():
    found = 0 # Determines whether the can has been found or not.
    speedX = speedY = 50 # Base speed rate.
    randomness = 15 # This is used to get out of a loop. More details later.
    drive(speedX, speedY) # Drive forward
    reset_gyro()
    while True:
        if cs.color == 5 and not found: # If the colour sensor detects red and we don't have the can.
            found = 1 # This avoids repeatedly finding the can when we already have it.
            angle_found = gs.value()
            Sound.tone([(400, 1000, 200)]) # Beep when can is found.
            sleep(0.3) # Go a tiny bit forward
            stop_motors()
            grab()
            angle_now = gs.value() # We get the angle after grabbing the can because
                                   # the robot might move while trying to grab it.
            turn_180(abs(angle_now-angle_found)) # Precisely turns in a southern direction.
        front, right = detect()
        if right > RIGHT_WALL_DIST: # Right side open
            if front > FRONT_WALL_DIST:
                # If front is a potential opening
                if random.randint(1, 16) <= randomness:
                    # This is how we get out of loops.
                    # We pick a random number between 1-16.
                    # If it's less than or equal to randomness (15 initially),
                    # Then it will turn right.
                    # However, if it's not, then it will go right.
                    # Thus, there's a 15/16 chance to go right
                    randomness -= 1
                    # However, after every right turn, we reduce randomness by 1.
                    # That means, next time we decide to turn right, there will be a
                    # 14/16 chance of going right, and a 2/16 chance of going straight.
                    # This assumes that straight is an open path, of course.
                    # This number stacks. Thus, after every consecutive right turn,
                    # The chance to go right will decrease and to go straight will increase.
                    # After any left turn, randomness will reset back to 15,
                    # because we are definitely not in a loop.
                    stop_motors()
                    kick() # Kick forward a little.
                    turn_right()
                else:
                    # We hit the roll with random.
                    # Go straight. HOWEVER, we need to drive forward to pass
                    # the open right space and not detect that as a turn.
                    randomness = 15
                    # Since we've gone straight, we reset the randomness back to 15 (base).
                    initTime = time()
                    while detect()[1] > RIGHT_WALL_DIST:
                        speedX, speedY = balance_gyro(speedX, speedY)
                        drive(speedX, speedY)
                        if detect()[1] <= RIGHT_WALL_DIST or time() - initTime >= 3:
                            # If we have gone past the corridor we just came out of,
                            # OR 3 seconds is up.
                            break
                        if detect()[0] < 100: # We're about to hit a wall in front of us.
                            # In a perfect world, this will never happen. But we add it in
                            # as a precaution.
                            break
            else:
                # Straight is not open at all. This is a simple case of just turning right.
                stop_motors()
                kick()
                turn_right()
        elif front < FRONT_WALL_DIST and right < RIGHT_WALL_DIST: # Front blocked, right blocked
            # Turn left
            randomness = 15 # We reset our randomness. We definitely are not in a loop.
            stop_motors()
            turn_left()
            front, right = detect()
            if front < FRONT_WALL_DIST: # We're in a dead end
                turn_left()
        elif front < FRONT_WALL_DIST:
            # If front is blocked. In a perfect world this won't occur,
            # because right will be detected first. However, it's a precaution.
            stop_motors()
            kick()
            turn_right()
        else:
            # Nowhere is open to turn. Continue driving forward while course-correcting.
            speedX, speedY = balance(speedX, speedY)
            drive(speedX, speedY)

if __name__ == '__main__':
    assert is_connected()
    print("Everything is connected. Starting...")
    try:
        main()
    except KeyboardInterrupt: # Manual input to stop the robot from driving. (CTRL+C)
        print("Ending...")
        stop_motors()
        clawMotor.stop()
        