from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 300
BASE_MOTOR_SPEED = 500

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

	return time()

def locate():
	""" 
	Locates the other robot and returns how long it took to find it.

	After finding it, the UltrasonicSensor is reverted back to its initial position (0)
	"""
	initialTime = time()
	sensorMotor.run_to_rel_pos(position_sp=350, speed_sp=BASE_MOTOR_SPEED) # rel_pos so it goes full cycle
	distance = 2550 # Don't make it us.value() in case while loop doesn't run
	while distance > ROBOT_DISTANCE:
		distance = us.value()
		print(distance)
		if distance <= ROBOT_DISTANCE: # FOUND 
			endTime = time()
			sensorMotor.stop()
			sensorMotor.run_to_abs_pos(position=0, speed_sp=1000)
			if sensorMotor.position() > 180: # NOT SURE IF WORKS
				direction = -1
			else:
				direction = 1
			return (endTime-initialTime, direction)

def turn(timeLength, direction):
	"""
	Turns the robot around towards the other robot.

	Determined through the time it took to find the other robot with the sensor.
	"""
	leftMotor.run_timed(speed_sp=direction*BASE_MOTOR_SPEED, time_sp=timeLength)
	rightMotor.run_timed(speed_sp=-1*direction*BASE_MOTOR_SPEED, time_sp=timeLength)
	return 1

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
	return "lost" # Position unknown

def main():
	"""
	Main function of the program.
	"""
	rightMotor = LargeMotor(OUTPUT_A)
	leftMotor = LargeMotor(OUTPUT_D)
	sensorMotor = Motor(OUTPUT_C); assert sensorMotor.connected
	us = UltrasonicSensor(INPUT_1); assert us.connected
	btn = Button()

	init = startup()
	timeTaken, half = locate()
	print("Time taken:", timeTaken)
	sleep(3 - (timeTaken - init))
	# Need to wait here until the 3 seconds are up
	turn(timeTaken, half)
	while True:
		if drive() == "lost":
			turn(*locate())
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