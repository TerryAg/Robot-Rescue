from ev3dev.ev3 import *
import time

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
	return time.time()

def locate():
	""" 
	Locates the other robot and returns how long it took to find it.

	After finding it, the UltrasonicSensor is reverted back to its initial position (0)
	"""
	initialTime = time.time()
	sensorMotor.run_to_rel_pos(position_sp=350, speed_sp=500) # rel_pos so it goes full cycle
	distance = us.value()
	while distance > 300:
		distance = us.value()
		print(distance)
		if distance <= 300: # FOUND 
			endTime = time.time()
			if sensorMotor.position() > 180:
				direction = -1
			else:
				direction = 1
			sensorMotor.stop()
			sensorMotor.run_to_abs_pos(position=0, speed_sp=1000)
			return (endTime-initialTime, direction)
	# can we get the current pos? sensorMotor.position_sp??
	# sensorMotor.position
	# or sensorMotor.position() ? according to github
	# if pos > 180, turn right. otherwise turn left.
#speed_regulation_enabled?

def turn(timeLength, direction):
	"""
	Turns the robot around towards the other robot.

	Determined through the time it took to find the other robot with the sensor.
	"""
	leftMotor.run_timed(speed_sp=direction*500, time_sp=timeLength)
	rightMotor.run_timed(speed_sp=-1*direction*500, time_sp=timeLength)
	return time.time()

def drive():
	"""
	Drives the robot in the current direction - fast.
	"""
	while us.value() < 300:
		leftMotor.run_direct(duty_cycle_sp=100)
		rightMotor.run_direct(duty_cycle_sp=100)
		time.sleep(0.1)
	return "Lost" # Position unknown


def main():
	"""
	Main function of the program.
	"""
	before = startup()
	timeTaken, half = locate()
	print("Time taken:", timeTaken)
	after = turn(timeTaken, half)
	time.sleep(3 - (after - before))
	# Need to wait here for until the 3 seconds is up
	while True:
		if drive() == "Lost":
			turn(*locate())
		if btn.backspace:
			leftMotor.stop()
			rightMotor.stop()
			break

if __name__ == '__main__':
	main()

#sensorMotor.run_direct(duty_cycle_sp=100)
#sensorMotor.run_to_abs_pos(position_sp=180)
#sensorMotor.run_timed(speed_sp=100, time_sp=600)