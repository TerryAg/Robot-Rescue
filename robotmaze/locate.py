from ev3dev.ev3 import *
from time import sleep

# Wall searching method

rightMotor = LargeMotor(OUTPUT_A); assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_B); assert leftMotor.connected
sensorMotor = Motor(OUTPUT_D); assert sensorMotor.connected
#us = UltrasonicSensor(INPUT_2); assert us.connected
#ls = LightSensor(INPUT_3); assert ls.connected
usTop = UltrasonicSensor(INPUT_1); assert usTop.connected # Rotating one.
gs = GyroSensor(); assert gs.connected # INPUT_1
gs.mode = 'GYRO-ANG'
btn = Button()

WALL_DISTANCE = 200
NODES = {}
NODE_LEVEL = 2 # since entrance is 1
NODE_LEVEL_PASSED = 1
input("turn to left")
left = sensorMotor.position
input("turn to mid")
mid = sensorMotor.position
input("turn to right")
right = sensorMotor.position
current_direction = [0]
#drive forward, rotate turret, if opening, that's a new node (including straight.)

class Node:
    def __init__(self, name, direction, parent, children=None):
    	self.name = name
    	self.direction = direction
    	self.parent = parent
        self.children = []
        if children is not None:
        	for child in children:
        		self.add_child(child)

    def add_child(self, node):
    	assert isintance(node, Tree)
    	self.children.append(node)

    # have like parents/children


#drive forward until new node met. (i.e, wall in front OR walls open on side)

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
        if usTop.value() < WALL_DISTANCE: # Not a wall #CHANGE THIS BACK TO > NOT < 
            results.append(angle)
    if not results: return sensor_turning(reverse=True if reverse==-1 else False)
    return results

def turn(angl): # Gyro scope?? turn until gyroscope
    if angl == left:
        direction = -1
    elif angl == right:
        direction = 1
    else:
    	return None # do ntohing
    leftMotor.run_timed(time_sp=1000, speed_sp=-direction*200)
    rightMotor.run_timed(time_sp=1000, speed_sp=direction*200)
    current_direction = [angl]

def drive_forward():
    leftMotor.run_direct(duty_cycle_sp=50)
    rightMotor.run_direct(duty_cycle_sp=50)
    sleep(2) # Give it some time.
    rever = False
    while True:
        spin = sensor_turning(rever)
        sleep(0.5)
        rever = False if rever else True # Swaps True--> False, False --> True
        if spin and spin != current_direction: # Not an empty list returned and not just straight opened.
        	# it's not always gonna be [0]... wait yes it will?
            # Found an opening
            # maybe need to drive a little more forward?
            # Create a Node for all open locs and the direction it taekes to turn into such a node

            leftMotor.stop() # Maybe don't let it stop 100%... slow down.
            rightMotor.stop()
            if len(spin) == 1: # only one direction to go to
                return spin[0] # the dir to go
            for loc in spin: # Don't bother about creating a node if only one path.
                # Create Node
                neighbours = [i for i in spin if i != loc]
                NODES[NODE_LEVEL] = Node(neighbours, loc)
                NODE_LEVEL += 1
            break
        sleep(0.5)
    print(NODES)
    # Scan to see where there are openings.

def explore(node1):
    # goes through node
    turn(node1.direction)
    drive_forward() # do something to tell it that we are in a node.

nodess = {
	'root': Node('root', mid)
}
#create new node inside of dict

def main2(): # basically the whole script... chop down later into functions
    leftMotor.run_direct(duty_cycle_sp=50)
    rightMotor.run_direct(duty_cycle_sp=50)
    sensor_results = sensor_turning()
    if len(sensor_results) == 1 and sensor_results != [mid]: # Left OR right open.
    	# do another condition to check if linear
    	# how else to determine parent
    	# current_parent = 
    	direc = sensor_results[0]
    	parent = 'root' if NODE_LEVEL == 1 else NODE_LEVEL-1
    	new_node = Node(1, direc, parent)
    	nodess[NODE_LEVEL] = new_node
    	nodess[parent].add_child(new_node)
   		NODE_LEVEL += 1
    	leftMotor.stop()
    	rightMotor.stop()
    	sleep(1) # Give it time to stop
    	turn(direc) # Change this to "explore the tree"
    	sleep(1) # Give it some time to turn
    	main2() # Now repeat
    elif len(sensor_results) == 2 and mid in sensor_results: # Left/mid or mid/right
    	NODE_LEVEL += 2 # Two new nodes
    	if left in sensor_results:# Mid, left
    		new_nodes = [Node(NODE_LEVEL-1, mid, []), Node(NODE_LEVEL, left, [])] # children
    		parent = node_level-3

    		# add these new_nodes to the neighbours of node_level-3.
    		#Loop through tree until we reach that node_level-3, then append new_nodes to its neighbours
    		# Make a func that does ^
    		
    		Node(1, [Node(2, mid, []), Node(3, left, [])])
    		# Where 1 is where we are at, 2 is straight, 3 is left.
    		# We don't know 2 and 3's neighbours.
    	# Create Node
    	# Go right/mid or mid/left
    	# go back to orig node
    elif len(sensor_results) == 3:
    	# Three paths.

"""
The maze Tree will probably be:

	0?
Node(1, 
	[Node(2,
		[Node(3,
			Node(4,
				[Node(5,
					[Node(6,
						[Node(7,
							[Node(8, []), Node(9,
											[Node(10, [])
)])])])])]))])])

"""
def dfs_recursive(node):
	print("Node:", node.id)
	if not node.neighbours:
		return None # done
		#actually, we ned to go back tp previous node
	for neighbour in node.neighbours:
		dfs_recursive(neighbour)


#TESTING:
main()





def new_node():
    pass

