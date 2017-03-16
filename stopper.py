from time import sleep
import sys, os
from ev3dev.ev3 import *

#Connect motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

# Connect touch sensors.
ts1 = TouchSensor(INPUT_1); assert ts1.connected
ts4 = TouchSensor(INPUT_4); assert ts4.connected
us = UltrasonicSensor(); assert us.connected
gs = GyroSensor(); assert gs.connected
gs.mode = 'GYRO-ANG'

# We will need to check EV3 buttons state.
btn = Button()


def start():
	"""
	Start both motors.
	`run-direct` allows varying motor performance on the fly
	by adjusting `duty_cycle_sp` attribute.
	"""
	rightMotor.run_direct(duty_cycle_sp=75)
	leftMotor.run_direct(duty_cycle_sp=75) 


def backup():
	"""
	Back away from an obstacle.
	"""
	Sound.tone([(1000, 500, 500)] * 3) # Sound backup alarm.
	Leds.set_color(Leds.RIGHT, Leds.RED) # Turn backup lights on
	Leds.set_color(Leds.LEFT, Leds.RED)
	# Stop both motors and reverse for 1.5 seconds.
	# `run-timed` command will return immediately, so we will have to wait
	# until both motors are stopped before continuing.
	rightMotor.stop(stop_command='brake')
	leftMotor.stop(stop_command='brake')
	rightMotor.run_timed(speed_sp = -500, time_sp=1500)
	leftMotor.run_timed(speed_sp = -500, time_sp=1500)
	# When motor is stopped, its `state` attribute returns empty list.
	# Wait until both motors are stopped:
	while any(m.state for m in (leftMotor, rightMotor)):
		sleep(0.1)
	Leds.set_color(Leds.RIGHT, Leds.GREEN) # Turn backup lights off
	Leds.set_color(Leds.LEFT, Leds.GREEN)

	
def turn(dir):
	"""
	Turn in the direction opposite to the contact.
	"""
	# We want to turn the robot wheels in opposite directions
	rightMotor.run_timed(speed_sp=dir*-750, time_sp=250)
	leftMotor.run_timed(speed_sp=dir*750, time_sp=250)
	# Wait until both motors are stopped:
	while any(m.state for m in (leftMotor, rightMotor)):
		sleep(0.1) 

# Run the robot until a button is pressed.
start()
while not btn.any():
	# If bump obstacle, back away
	# turn and go in other direction.
	if ts1.value():
		backup()
		turn(1)
		start()
	if ts4.value():
		backup()
		turn(-1)
		start() 


	# Use compass to keep the robot going
	# in the same direction
	direction = gs.value();
	# print direction
	if direction > 5:
		# print('right')
		rightMotor.duty_cycle_sp = 5
	elif direction < 5:
		# print('left')
		leftMotor.duty_cycle_sp = 5
	else:
		leftMotor.duty_cycle_sp = 75
		rightMotor.duty_cycle_sp = 75
		# Ultrasonic sensor will measure distance
		# to the closest object in front of it.
		distance = us.value()
	if distance > 300:
		# Path is clear, run at full speed.
		dc = 75
	else:
		# Obstacle ahead, slow down.
		dc = 30
	for m in (leftMotor, rightMotor):
		m.duty_cycle_sp = dc
		print(rightMotor.position, leftMotor.position)


# On exit from the while loop
# stop the motors before exiting.
rightMotor.stop()
leftMotor.stop() 