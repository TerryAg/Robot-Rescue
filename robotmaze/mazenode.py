# This script implements a Depth-first search (DFS), but it was
# never used - largely because of inaccuracies with the robot.

from ev3dev.ev3 import *
from time import sleep, time
import sys

rightMotor = LargeMotor(OUTPUT_D)
leftMotor = LargeMotor(OUTPUT_A)
clawMotor = Motor(OUTPUT_B)
sensorMotor = Motor(OUTPUT_C)

usTop = UltrasonicSensor(INPUT_2)
cs = ColorSensor(INPUT_4)
gs = GyroSensor()
gs.mode = 'GYRO-ANG'

class Node:
    def __init__(self, id, parent, directions):
        self.id = id
        self.parent = parent
        self.directions = directions # list eg [mid, left]

class CanFound(Exception):
    pass

def sensor_turning(reverse=False):
    #usTop rotating
    # Make it go to three points: West, North, East
    results = []
    if not reverse:
        reverse = -1
    else:
        reverse = 1
    for angle in [left, mid, right][::-reverse][1:]: # West, North, East
        sensorMotor.run_to_abs_pos(position_sp=angle, speed_sp=300)
        sleep(0.5)
        if usTop.value() > WALL_DISTANCE:
            results.append(angle)
    if not results: return sensor_turning(reverse=True if reverse==-1 else False)
    return results

def reset_gyro():
    # By changing the mode of the gyroscope, the values reset back to 0.
    gs.mode = 'GYRO-RATE'
    gs.mode = 'GYRO-ANG'

def is_connected():
    for connection in (rightMotor, leftMotor, clawMotor, usTop, cs, gs):
        if not connection.connected:
            print("{} is not connected.".format(connection))
            sys.exit(zero)
    return True

def stop_motors():
    leftMotor.stop()
    rightMotor.stop()
    sleep(0.5)


"""
Experiment:

def q():
    reset_gyro()
    while gs.value() != -90:
        if gs.value() > -90:
            leftMotor.run_direct(duty_cycle_sp=-30) # make it only move left wheel not right
            rightMotor.run_direct(duty_cycle_sp=30)
        if gs.value() < -90:
            leftMotor.run_direct(duty_cycle_sp=30) # make it only move left wheel not right
            rightMotor.run_direct(duty_cycle_sp=-30)
        if gs.value() > -90:
            leftMotor.run_direct(duty_cycle_sp=-30) # make it only move left wheel not right
            rightMotor.run_direct(duty_cycle_sp=30)
    stop_motors()    
    reset_gyro()
...
etc
"""
def turn_left(reset=True):
    print("turning left")
    if reset:
        reset_gyro()
    while gs.value() > -90:
        leftMotor.run_direct(duty_cycle_sp=-30) # make it only move left wheel not right
        rightMotor.run_direct(duty_cycle_sp=30)
        if gs.value() <= -90:
            stop_motors()
            break
    while gs.value() < -90: # it went over
        leftMotor.run_direct(duty_cycle_sp=15) # make it only move left wheel not right
        rightMotor.run_direct(duty_cycle_sp=-15)
        if gs.value() >= -90:
            stop_motors()
            break
    stop_motors()
    reset_gyro()
    sens_results_after_turn = sensor_turning()
    if mid not in sens_results_after_turn:
        # IT'S A DEAD END!!!
        # WE DON'T WANT TO DO A 180º TURN HERE BECAUSE OTHER FUNCTIONS WILL DO THAT!
        print("This is a dead end@@76345834ioy")
        return
    init_time = time()
    while time()-init_time < 1: # drive a bit past the bit we just turned out of
        drive(*balance(70,70))
        if time()-init_time >= 1:
            return


def turn_right():
    print("turning right")
    #leftMotor.run_direct(duty_cycle_sp=70) # copy this to turn_left
    #rightMotor.run_direct(duty_cycle_sp=70) # FIX THIS
    stop_motors()
    reset_gyro()
    while gs.value() < 90:
        leftMotor.run_direct(duty_cycle_sp=30)
        rightMotor.run_direct(duty_cycle_sp=-30)
        if gs.value() >= 90: # Not really needed for a while loop... but gives accuracy immediately
            stop_motors()
            break
    while gs.value() > 90: # It went a little too far... backtrack back to 90
        leftMotor.run_direct(duty_cycle_sp=-15) # Go slower this time
        rightMotor.run_direct(duty_cycle_sp=15)
        if gs.value() <= -90:
            stop_motors()
            break
    stop_motors()
    reset_gyro() # We reset for balance()
    sens_results_after_turn = sensor_turning()
    if mid not in sens_results_after_turn:
        # IT'S A DEAD END!!!
        # WE DON'T WANT TO DO A 180º TURN HERE BECAUSE OTHER FUNCTIONS WILL DO THAT!
        print("This is a dead end@@76345834ioy")
        return
    init_time = time()
    while time()-init_time < 1: # drive a bit past the bit we just turned out of
        drive(*balance(70,70))
        if time()-init_time >= 1:
            return

def is_can():
    if cs.color == 5: # Red
        print("Can found!!")
        return True
    return False

def grab():
    clawMotor.run_direct(duty_cycle_sp=-100)
    sleep(3)
    clawMotor.duty_cycle_sp=-30 # Still give it some pressure so can doesn't fall out of grasp

"""
def detect():
    return usFront.value()*10, usRight.value()
"""

def drive(speedX, speedY):
    leftMotor.run_direct(duty_cycle_sp=speedX)
    rightMotor.run_direct(duty_cycle_sp=speedY)

def balance(speedX, speedY):
    # Try experiment 1/-1
    if gs.value() > 2: # It's drifting right, so go left
        speedX = 60 # Try 65?
        print("steering left")
    elif gs.value() < -2: # It's drifting left, so go right
        speedY = 60
        print("Steering right)")
    else: # It's all good
        speedX = speedY = 70
    return speedX, speedY

class Node:
    def __init__(self, id, directions, neighbours=None):
        self.id = id
        self.directions = directions # NOT LIST
        assert isinstance(directions, str)
        if neighbours is not None:
            self.neighbours = neighbours

def simple_traverse():
    # For going through a bit of the maze one dimensional
    print("Simple traversing time!")
    while True:
        intersections = sensor_turning()
        if len(intersections) >= 2: return
        if is_can(): # In a perfect world this will never happen because we're backtracking through paths
                     # we've gone through already.
            raise CanFound
        if intersecions == [right]:
            stop_motors()
            turn_right()
        elif intersections == [left]:
            stop_motors()
            turn_left()
        else:
            drive(*balance(speedX, speedY))

def recurs_DFS(node):
    # TODO
    # Fix turn left/right and give it some immunity time before sensor_motor kicks in
    # ^^ done
    # I don't think this needs editing for that^... but turn_left/turn)right does (eg it still uses detect())
    for neighbour in node.neighbours: # neighbour is a NODE
        if neighbour.direction is None: continue # passed
        if neighbour.direction == left:
            turn_left()
            sleep(5) # give it time to turn
        elif neighbour.direction == right:
            turn_right()
            sleep(5) # give it time to turn
        elif neighbour.direction == mid:
            drive(*balance(70,70))
        while True:
            # keep driving until intersection
            drive(*balance(70,70))
            intersections = sensor_turning()
            if is_can():
                raise CanFound
            if not intersections: # DEAD END
                # we have to turn around and somehow go back to previous node??
                # the parent.......
                print("We've hit a dead end")
                stop_motors()
                turn_left()
                turn_left()
                print("Traversing back to first intersection")
                simple_traverse() # this returns us to first junction
                print("Done traversing back")
                node.neighbours[node.neighbours.index(neighbour.direction)] = None # We've finished with it
                # now turn in the direction we first encountered the node.
                if neighbour.direction == right: #
                    turn_right()
                    sleep(2)
                    print("Node done, exploring next one")
                elif neighbour.direction == left:
                    turn_left()
                    sleep(2)
                    print("Node done, exploring next one")
                elif neighbour.direction == mid:
                    turn_left()
                    turn_left()
                    sleep(2)
                    print("Node done, exploring next one")

                # now we're facing original point. It is safe to explore the rest of the chidren nodes.
                return recurs_DFS(node)
            if intersections == [right]:
                print("There's just one way to go - GO RIGHT")
                stop_motors()
                turn_right()
            elif intersections == [left]:
                print("There's just one way to go - GO LEFT")
                stop_motors()
                turn_left()

            if len(intersections) == 2:
                # Create two new nodes
                new_node1 = Node(NODE_COUNT, intersections[0]) # don't need parent since we're already in n.
                NODE_COUNT += 1
                new_node2 = Node(NODE_COUNT, intersections[1])
                NODE_COUNT += 1
                neighbour.neighbours = [new_node1, new_node2] #... do we need IDs then? or just helpful
                #migjt need IDs for when we backtracking
                return recurs_DFS(neighbour) # return?
            elif len(intersections) == 3:
                new_node1 = Node(NODE_COUNT, intersections[0])
                NODE_COUNT += 1
                new_node2 = Node(NODE_COUNT, intersections[1])
                NODE_COUNT += 1
                new_node3 = Node(NODE_COUNT, intersections[2])
                NODE_COUNT += 1
                neighbour.neighbours = [new_node1, new_node2, new_node3]
                return recurs_DFS(neighbour)

def find_path(tree):
    """
    Finds the most efficient path back throught the tree to the root
    """
    results = []
    for neighbour in tree.neighbours:
        continue
        # TODO
    results.reverse()
    pass

if __name__ == '__main__':
    is_connected()
    reset_gyro()
    input("turn to left") # mvoe this all into bottom if clause
    left = sensorMotor.position
    input("turn to mid")
    mid = sensorMotor.position
    input("turn to right")
    right = sensorMotor.position

    print("Everything is connected. Starting...")
    Tree = Node('root', mid, neighbours=Node(1, mid))
    NODE_COUNT = 2
    try:
        recurs_DFS(Tree)
    except KeyboardInterrupt:
        stop_motors()
        clawMotor.stop()
        print("Ending...")
    except CanFound:
        # Error raised when can is found. We now search tree for efficient path ? or just node our way out
        grab()
        turn_left(reset=False)
        turn_left()
        simple_traverse()
        # Turns south exactly.
        # now find best path back.
        #loop through tree and find all the paths that are not None (however there may be paths that are not none but we have not explored them yet)

        # wait we can fix this by first simple_traverseing back to the first instersction adn that wau eevery other node past that there will only be one option to go.
        find_path(Tree)





