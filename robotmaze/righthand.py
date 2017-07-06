# This script was used in the preliminary round, where
# only finding the can was necessary for the task.
# It implemented a right-hand wall method, which was
# also ultimately used in the final too.

from ev3dev.ev3 import *
from time import sleep, time

rightMotor = LargeMotor(OUTPUT_A); assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_B); assert leftMotor.connected
usBottom = UltrasonicSensor(INPUT_3); assert usBottom.connected
usTop = UltrasonicSensor(INPUT_2); assert usTop.connected # Rotating one.
cs = ColorSensor(); assert cs.connected
print(cs.ambient_light_intensity)
btn = Button()
#gs = GyroSensor(); assert gs.connected
#gs.mode = 'TILT-ANG'

def stop_motors():
    leftMotor.stop()
    rightMotor.stop()
    sleep(0.3)

c = 895
def turn(direction):
    global c
    sleep(0.5)
    leftMotor.run_timed(time_sp=c, speed_sp=-direction*200)
    rightMotor.run_timed(time_sp=c, speed_sp=direction*200)
    sleep(1)
    # confirm if it turned correctly
    c-=5
    return (c-5)
   # gs = GyroSensor()
   # gs.mode = 'TILT-ANG'

def kick(direction):
    leftMotor.run_timed(time_sp=200, speed_sp=-direction*200)
    rightMotor.run_timed(time_sp=200, speed_sp=direction*200)

def kick_forward(direction):
    leftMotor.run_timed(time_sp=1000, speed_sp=direction*300)
    rightMotor.run_timed(time_sp=1000, speed_sp=direction*300)

def backwards():
    leftMotor.run_timed(time_sp=3000, speed_sp=-1000)
    rightMotor.run_timed(time_sp=3000, speed_sp=-1000) 

def detect_can():
    if cs.color == 5: #red
        return True
        # Can found!
        # Make noise.
    else:
        return False

def detect_and_turn():
    # reverse > < back to < >
    if cs.color == 5:
        Sound.tone([(400, 1000, 200), (800, 1000, 500), (1000, 1000, 100),(500, 1000, 500)])
        return "done"
    if usTop.value()*10 > 400: # We prioritise going right before going straight, if possible
        print("Turning right!")
        stop_motors()
       # kick_forward(1)# go forward a little more to give us space
        sleep(0.5)
        turn(-1)
        init = time()
        while usTop.value()*10 > 200:
            print(4)
            if usTop.value()*10 < 200: break
            leftMotor.run_timed(time_sp=100, speed_sp=300)
            rightMotor.run_timed(time_sp=100, speed_sp=300)
            if time()-init >= 4: 
                stop_motors()
                backwards()
                break
        print("--")
        return True
    elif usBottom.value() < 190: # about to hit wall
        stop_motors()
        if usTop.value()*10 > 400: # We prioritise going right before going straight, if possible
            print("actually going right!")
            stop_motors()
           # kick_forward(1)# go forward a little more to give us space
            sleep(0.5)
            turn(-1)
            init = time()
            while usTop.value()*10 > 200:
                print(7)
                if usTop.value()*10 < 200: break
                leftMotor.run_timed(time_sp=100, speed_sp=300)
                rightMotor.run_timed(time_sp=100, speed_sp=300)
                if time()-init >= 4: 
                    stop_motors()
                    backwards()
                    break
            print("------")
            return True
        print("Turning left because of wall infront!")
        #kick_forward(1)
        turn(1)
        # Scan again just in case when we turn left it's not a wall again (i.e we're in a dead end)
        test=0
        while usBottom.value() < 190:
            print("kick!")
            test=1
            kick(1)
        if test==1:
            print("final turn")
            turn(1)
        return True
    else:
        return None


def balance(CURRENT_SPEEDL, CURRENT_SPEEDR):
    # Keeps us on track.
    # should only be called when driving in  a straight line.
    stack = []
    while True:
        stack.append(usTop.value())
        difference = stack[-1] - stack[0]
        if difference >= 2: #big variance
            #it's going too far right.
            print("too far right")
            CURRENT_SPEEDR += 2
            CURRENT_SPEEDL -= 2
            return (CURRENT_SPEEDL, CURRENT_SPEEDR)
        if difference <= -2:
            #too far left
            print("Too far left")
            CURRENT_SPEEDL += 2
            CURRENT_SPEEDR -= 2
            return (CURRENT_SPEEDL, CURRENT_SPEEDR)
        if len(stack) > 300: #had enough attempts for nothing to happen
            print("All good")
            return (CURRENT_SPEEDL, CURRENT_SPEEDR)

def main():
    CURRENT_SPEEDL = 50
    CURRENT_SPEEDR = 50
    leftMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDL)
    rightMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDR)
    sleep(1)
    while True:
        if cs.color == 5:
            Sound.tone([(400, 1000, 200), (800, 1000, 500), (1000, 1000, 100), (500, 1000, 500)])
            stop_motors()
            print("FOUND")
            break
        """direction = gs.value()
                                #print(direction)
                                if direction < -5:
                                    print("too far left dritfting")
                        
                                    CURRENT_SPEEDL += 3
                                    CURRENT_SPEEDR -= 2
                                elif direction > 5:
                                    print("too far right dritfting")
                                    CURRENT_SPEEDL -= 2
                                    CURRENT_SPEEDR += 3"""
        res = detect_and_turn()
        if res == "done": 
            stop_motors()
            print("FOUND")
            sleep(3)
            Sound.speak("Found it!").wait()
            break
        if res is not None:
            leftMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDL)
            rightMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDR)
            if cs.color == 5:
                Sound.tone([(400, 1000, 200), (800, 1000, 500), (1000, 1000, 100), (500, 1000, 500)])
                stop_motors()
                print("FOUND")
                break
             # give it time to pass the space we were just in\
            # might need to be longer? depends on speed of robot honestly.
        else:
            #CURRENT_SPEEDL, CURRENT_SPEEDR = balance(CURRENT_SPEEDL, CURRENT_SPEEDR) 
            leftMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDL)
            rightMotor.run_direct(duty_cycle_sp=CURRENT_SPEEDR)
    """
    while detect_and_turn() is not None: # While we haven't hit a wall in front
        if detect_can():
            stop_motors()
            Sound.tone([(1000, 500, 500)] * 3)
            break #done
    """



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        stop_motors()
