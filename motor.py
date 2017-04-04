from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 100 # Distance between one robot and the other.

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C); assert sensorMotor.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
btn = Button()

def startup():
	"""
	A function run at the beginning of the program to determine
	when to start through user input.

	The robot must stay still for 3 seconds before it can move.

	Returns the current time when the backspace button is pressed,
	so that we may sleep for as little as possible until 3 seconds is up.s
	"""
	backspace_pressed = False
	print("Ready to start. Press the backspace button to resume.")
	while not backspace_pressed:
		backspace_pressed = btn.backspace

	return time()

def locate_first():
	"""
	Locates the other robot during the first three seconds. Only the sensorMotor runs.

	Returns the position at which the other robot is found.
	"""
	sensorMotor.run_to_abs_pos(position_sp=160, speed_sp=250)
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
			print("Turning around")
			sensorMotor.run_to_abs_pos(position_sp=-270, speed_sp=250)
			if not sensorMotor.state:
				return locate_first() # Needs testing.

def locate_subsequent():
	"""
	Different to first locate since now we are turning while locating 
	-- not using sensorMotor
	"""
	leftMotor.run_timed(time_sp=10000, speed_sp=-550) # Perhaps change dir depending on
	rightMotor.run_timed(time_sp=10000, speed_sp=550) # last location seen?
	while True:
		distance = us.value()
		if distance < ROBOT_DISTANCE:
			leftMotor.stop()
			rightMotor.stop()
			return 1

def turn(pos, direction):
	"""
	Turns the robot around towards the other robot.

	Determined through the position of the sensorMotor when it found the other robot.
	"""
	leftMotor.run_to_abs_pos(position_sp=pos*direction)
	rightMotor.run_to_abs_pos(position_sp=-1*pos*direction)
	while any(m.state for m in (leftMotor, rightMotor)):
		continue # Let the motors completely turn before doing drive()

def drive():
	"""
	Drives the robot in the current direction as fast as it can.
	"""
	while us.value() < ROBOT_DISTANCE:
		leftMotor.run_direct(duty_cycle_sp=100)
		rightMotor.run_direct(duty_cycle_sp=100)
		sleep(0.1)

	print("Can't find other robot... Relocating")
	leftMotor.stop()
	rightMotor.stop()
	return "lost" # Position unknown.

def main():
	"""
	Main function of the program.
	"""
	sensorMotor.position = 0
	leftMotor.position = 0
	rightMotor.position = 0 # Defining the starting point as 0.
	init = startup()
	enemy_pos, direction = locate_first()
	sensorMotor.run_to_abs_pos(position_sp=10) # Reset sensorMotor back to front.
	sleep(3-(time()-init))
	turn(2.5*enemy_pos, direction) # 2.5 MIGHT NEED CHANGING DEPENDING ON SURFACE OF PLAYING AREA
	while True:
		try: # Test this.
			if drive() == "lost":
				locate_subsequent()
		except KeyboardInterrupt:
			leftMotor.stop()
			rightMotor.stop()
			print("Stopping...")
			break

if __name__ == '__main__':
	main()