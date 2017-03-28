from ev3dev.ev3 import *
import time
import sys

#Connect motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C)

# Connect touch sensors.
#ts1 = TouchSensor(INPUT_1); assert ts1.connected
#ts4 = TouchSensor(INPUT_4); assert ts4.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
gs = GyroSensor(INPUT_2); assert gs.connected
gs.mode = 'GYRO-ANG'
original_angle = gs.angle
print("ANGLE:", original_angle)

btn = Button()

def start(angle_found):
	"""
	Start both motors.
	`run-direct` allows varying motor performance on the fly
	by adjusting `duty_cycle_sp` attribute.
	"""
	rightMotor.run_direct(duty_cycle_sp=int(angle_found))
	leftMotor.run_direct(duty_cycle_sp=int(angle_found))

#check around until us.distance() is close

backspace_click = False

print("READY: ")
while not backspace_click:
	if btn.backspace:
		backspace_click = True
		time.sleep(3)

found = False

while True:
	 #must be -100 to 100
	sensorMotor.run_timed(speed_sp=500, time_sp=200)
	time.sleep(0.1)
	distance = us.value()
	print(distance)
	
	if distance < 300:
		# FOUND ROBOT
		print("ANGLE FOUND AT:", gs.angle)
		angle_found = gs.angle-original_angle
		print("DIFFERENCE:", gs.angle-original_angle)
		Sound.speak("FOUND").wait()
		sensorMotor.run_timed(speed_sp=-500, time_sp=300)
		time.sleep(0.1)
		found = True
		break
		# then get angle and turn wheels there after the 3 seconds

sensorMotor.run_timed(speed_sp=0)
#while sensorMotor.state:
#	time.sleep(0.1)
#	print(333)
time.sleep(0.1)
start(angle_found)
"""if not found: 
	sensorMotor.run_direct(duty_cycle_sp=-90)
	time.sleep(0.5)

while not found: #not found... try second loop
	distance = us.value()
	if distance < 100:
		# FOUND IT
		Sound.speak("I found you! Prepare to die!").wait()
		time.sleep(0.5)
		print(222222222)
		found = True
		sensorMotor.run_direct(duty_cycle_sp=-90)
		time.sleep(0.5)
		break
"""
sensorMotor.run_direct(duty_cycle_sp=0)

"""while True:
	sensorMotor.run_direct(duty_cycle_sp=-90)
	distance = us.value()
	if distance < 100:
		sensorMotor.run_direct(duty_cycle_sp=0)
		break"""
		# then get angle and turn wheels there after the 3 seconds
#distance = us.value()
	#print(distance)
		#start()




#rightMotor.stop()
#leftMotor.stop()