from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 500 # Distance between one robot and the other.
					 # 500 units is approximately 50cm (margin of error, of course).

rightMotor = LargeMotor(OUTPUT_A); assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D); assert leftMotor.connected
sensorMotor = Motor(OUTPUT_C); assert sensorMotor.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
btn = Button()


def startup():
	"""
	A function run at the beginning of the program to determine
	when to start through user input.

	The robot must stay still for 3 seconds before it can move.

	Returns the current time when the backspace button is pressed,
	so that we may sleep for as little as possible until 3 seconds is up.
	"""
	backspace_pressed = False
	print("Ready to start. Press the backspace button to resume.")
	while not backspace_pressed:
		backspace_pressed = btn.backspace

	sleep(1) # Gives the presser some time to get out of the way.
	return time()


def locate_first():
	"""
	Locates the other robot during the first three seconds. Only the sensorMotor runs.

	Returns the position at which the other robot is found, along with the direction.
	"""
	sensorMotor.run_to_abs_pos(position_sp=160, speed_sp=250) # Turns 160 degrees right.
	while True:
		distance = us.value() # Gets the distance from the Ultrasonic Sensor 
							  # and whatever it can see. 
		if distance < ROBOT_DISTANCE: # If there is something 500 units within sight.
			sensorMotor.stop()
			pos = sensorMotor.position
			sensorMotor.run_to_abs_pos(position_sp=0) # Reset sensorMotor back to front.
			if pos >= 0:
				return sensorMotor.position+30, 1 # We return the position+30 because
												  # of a margin of error. 
												  # It will never be precise.
			else:
				return abs(sensorMotor.position)+30, -1 # -1/1 determines what 'quadrant'
														# the sensor found the other robot.
		if not sensorMotor.state: # If the sensor stops moving and it hasn't found anything.
			sensorMotor.run_to_abs_pos(position_sp=-270, speed_sp=250)
			if not sensorMotor.state: # Again... if it hasn't found anything... reset.
				return locate_first()
			

def turn(pos, direction):
	"""
	Turns the robot around towards the other robot.

	Determined through the position of the sensorMotor when it found the other robot.
	"""
	leftMotor.run_to_abs_pos(position_sp=pos*direction, speed_sp=1000)
	rightMotor.run_to_abs_pos(position_sp=-1*pos*direction, speed_sp=1000)
	sleep(1) # We sleep here to give the robot time to turn.
	

def locate_subsequent(direction):
	"""
	Turns the robot around until it finds the other robot.

	This is different to locate() since the sensorMotor does not run.
	Instead, the wheels do.
	"""
	while True:
		leftMotor.run_direct(duty_cycle_sp=direction*100) 
		rightMotor.run_direct(duty_cycle_sp=-1*direction*100)
		distance = us.value()
		if distance < ROBOT_DISTANCE:
			leftMotor.stop()
			rightMotor.stop()
			return 1 # Breaks the loop.
		sleep(0.1)
		

def drive():
	"""
	Drives the robot in the current direction as fast as it can.
	"""
	while us.value() < ROBOT_DISTANCE: # This loop will run 
									   # while the other robot is in sight.
		leftMotor.run_direct(duty_cycle_sp=100)
		rightMotor.run_direct(duty_cycle_sp=100)
		sleep(0.1)

	print("Can't find other robot... Relocating")
	leftMotor.stop()
	rightMotor.stop()
	return "lost"


def main():
	"""
	Main function of the program.
	"""
	sensorMotor.position = 0
	leftMotor.position = 0
	rightMotor.position = 0 # Defining the starting point as 0.
	initialTime = startup()
	enemy_pos, direction = locate_first()
	try:
		sleep(2-(time()-initialTime))
	except ValueError: # It took longer than 3 seconds
		pass
	if direction == -1:
		turn(2*enemy_pos, direction) # Since it needed to turn more,
									 # there will be a bigger drift. Thus, we turn it
									 # for a lower amount.
	else:
		turn(2.5*enemy_pos, direction)
	while True:
		try:
			if drive() == "lost":
				locate_subsequent(direction)
		except KeyboardInterrupt: # Gives us the option to cancel the script whenever we
								  # want by doing CTRL+C.
			leftMotor.stop()
			rightMotor.stop()
			print("Stopping...")
			break

			
if __name__ == '__main__': # "if we are running the script directly"
	main() # This is useful since it prevents other files from running this code.
