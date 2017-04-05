from ev3dev.ev3 import *
import time

rightMotor = LargeMotor(OUTPUT_A); assert rightMotor.connected
leftMotor = LargeMotor(OUTPUT_D); assert leftMotor.connected
sensorMotor = Motor(OUTPUT_C); assert sensorMotor.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
btn = Button()

def forward(d):
	rightMotor.run_direct(duty_cycle_sp=100)
	leftMotor.run_direct(duty_cycle_sp=100)

def turn():
	rightMotor.run_direct(duty_cycle_sp=100)
	leftMotor.run_direct(duty_cycle_sp=-100)

def absolute_pos(pos):
	rightMotor.run_to_abs_pos(position_sp=pos)
	leftMotor.run_to_abs_pos(position_sp=-pos)

def sensor():
	sensorMotor.run_to_abs_pos(position_sp=181)
	time.sleep(2)
	sensorMotor.run_to_abs_pos(position_sp=-1)

def stop():
	rightMotor.stop()
	leftMotor.stop()
	sensorMotor.stop()

while True:
	inp = input("run: ")
	if inp == "forward":
		forward()
	elif inp == "turn":
		turn()
	elif inp == "abs":
		absolute_pos(int(input("Enter pos")))
	elif inp == "sensor":
		sensor()
	elif inp == "stop":
		stop()