from ev3dev.ev3 import *
from time import sleep, time

ROBOT_DISTANCE = 500
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
	return time()

def locate():
	directionn = 1
	initialTime = time()
	sensorMotor.run_to_rel_pos(position_sp=90, speed_sp=500)
	distance = 2550
	while distance > ROBOT_DISTANCE:
		distance = us.value()
		print(distance)
		if sensorMotor.position == 90: break
		if distance <= ROBOT_DISTANCE:
			endTime = time()
			sensorMotor.stop()
			print(sensorMotor.position)
			return (endTime-initialTime)*3000, directionn
	sensorMotor.run_to_rel_pos(position_sp=-180, speed_sp=500) # doesn't work atm
	initialTime = time()
	# swap direction too
	while distance > ROBOT_DISTANCE:
		distance = us.value()
		print(distance)
		if sensorMotor.position == 270: break
		if distance <= ROBOT_DISTANCE:
			endTime = time()
			sensorMotor.stop()
			print(sensorMotor.position)
			directionn = -1
			return (endTime-initialTime)*3000, directionn

def turn(timeLength, DIR):
	"""
	Turns the robot around towards the other robot.

	Determined through the time it took to find the other robot with the sensor.
	"""
	leftMotor.run_timed(speed_sp=DIR*BASE_MOTOR_SPEED, time_sp=timeLength)
	rightMotor.run_timed(speed_sp=-1*DIR*BASE_MOTOR_SPEED, time_sp=timeLength)
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
	#DIR = 1
	print(sensorMotor.position)
	#sensorMotor.run_to_abs_pos(position_sp=-25)
	init = startup()
	timeTaken, ddir = locate()
	print("Time taken:", timeTaken)
	#sleep(3 - (timeTaken - init))
	# Need to wait here until the 3 seconds are up
	#input("READY TO TURN FIRST TIME")
	turn(timeTaken, ddir)
	#input("IT HAS TURNED FOR THE FRIST TIME!!!")
	while True:

		if drive() == "lost":
			#DIR = -1 if DIR == 1 else 1
			#input("IT IS LOST... RELOCATING")
			a, bb = locate()
			#input("LOCATED!!!")
			turn(a, bb)
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