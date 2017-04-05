from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 700 # Distance between one robot and the other.

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
	so that we may sleep for as little as possible until 3 seconds is up.s
	"""
	backspace_pressed = False
	print("Ready to start. Press the backspace button to resume.")
	while not backspace_pressed:
		backspace_pressed = btn.backspace

	sleep(1)
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
				return sensorMotor.position+30, 1
			else:
				return abs(sensorMotor.position)+30, -1
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
	leftMotor.run_timed(time_sp=10000, speed_sp=-1050) # Perhaps change dir depending on
	rightMotor.run_timed(time_sp=10000, speed_sp=1050) # last location seen?
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
	leftMotor.run_to_abs_pos(position_sp=pos*direction, speed_sp=1000)
	rightMotor.run_to_abs_pos(position_sp=-1*pos*direction, speed_sp=1000)
	sleep(0.5)
	input("Did it turn well?")

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
	print(enemy_pos, direction)
	sensorMotor.run_to_abs_pos(position_sp=0) # Reset sensorMotor back to front.
	# Can we move ^ into locate_first?
	try:
		sleep(2-(time()-init))
	except ValueError: # It took longer than 3 seconds
		pass
	print("done sleeping")
	turn(3*enemy_pos, direction) # 2.5 MIGHT NEED CHANGING DEPENDING ON SURFACE OF PLAYING AREA
	#sleep(0.5)
	print("done turning")
	while True:
		try: # Test this.
			res = drive()
			if res == "lost":
				locate_subsequent()
		except KeyboardInterrupt:
			leftMotor.stop()
			rightMotor.stop()
			print("Stopping...")
			break

if __name__ == '__main__':
	main()