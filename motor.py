from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 300
BASE_MOTOR_SPEED = 150

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C); assert sensorMotor.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
btn = Button()


def startup():
    """
    A function run at the beginning of the program to determine
    when to start through user input.

    The robot must stay still for 3 seconds before it can move
    """
    backspace_pressed = False
    print("Ready to start. Press the backspace button to resume.\n")
    while not backspace_pressed:
        backspace_pressed = btn.backspace

    sleep(3)

def locate_first():
    sensorMotor.run_to_abs_pos(position_sp=160, speed_sp=250)
    direction = None
    while True:
        distance = us.value()
        if distance < ROBOT_DISTANCE:
            sensorMotor.stop()
            pos = sensorMotor.position
            if pos >= 0:
                return sensorMotor.position, 1
            else:
                return abs(sensorMotor.position), -1
        if not sensorMotor.state:
            print("turning around")
            sensorMotor.run_to_abs_pos(position_sp=-159, speed_sp=250)

def locate_subsequent():
    """
    Different to first locate since now we are turning while locating 
    -- not using sensorMotor
    """
    leftMotor.run_to_rel_pos(position_sp=360, speed_sp=250)
    rightMotor.run_to_rel_pos(position_sp=-360, speed_sp=250)
    while True:
        distance = us.value()
        if distance < ROBOT_DISTANCE:
            leftMotor.stop()
            rightMotor.stop()
            #sleep()?
            return 1

def turn(n, d):
    """
    Turns the robot around towards the other robot.

    Determined through the time it took to find the other robot with the sensor.
    """
    leftMotor.run_to_abs_pos(position_sp=n*d)
    rightMotor.run_to_abs_pos(position_sp=-1*n*d)
    return 1

def drive():
    """
    Drives the robot in the current direction as fast as it can.
    """
    while us.value() < ROBOT_DISTANCE:
        leftMotor.run_direct(duty_cycle_sp=20)
        rightMotor.run_direct(duty_cycle_sp=20)
        sleep(0.1)

    print("Can't find other robot... Relocating")
    leftMotor.stop()
    rightMotor.stop()
    return "lost" # Position unknown

def main():
    """
    Main function of the program.
    """
    sensorMotor.position = 0
    leftMotor.position = 0
    rightMotor.position = 0 # Defining the starting point as 0
    startup()
    pos, dirr = locate_first()
    print(pos, dirr)
    sensorMotor.run_to_abs_pos(position_sp=0, speed_sp=700)
    #sleep(3 - (timeTaken - init))
    # Need to wait here until the 3 seconds are up
   # input("READY TO TURN FIRST TIME")
    turn(3*pos, dirr)
    #input("IT HAS TURNED FOR THE FRIST TIME!!!")
    while True:
     #   input("READY TO DRIVE?")
        if drive() == "lost":
      #      input("IT IS LOST... RELOCATING")
            locate_subsequent()
       #     input("LOCATED!!!")

            #input("IT HAS TURNED")
        if btn.backspace: # Might need to change this to 'elif' if not possible
                            # to turn program off while it's in drive()
            leftMotor.stop()
            rightMotor.stop()
            print("Stopping...")
            break

if __name__ == '__main__':
    main()

#speed_regulation_enabled?
# Can run_timed take position? prob not