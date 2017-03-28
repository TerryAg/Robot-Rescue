from ev3dev.ev3 import *
import time
import sys

#Connect motors
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C)

class G: # temporary
	def __init__(self, tempp):
		self.mode = 'hi'
		self.angle = 50

# Connect touch sensors.
#ts1 = TouchSensor(INPUT_1); assert ts1.connected
#ts4 = TouchSensor(INPUT_4); assert ts4.connected
us = UltrasonicSensor(INPUT_1); assert us.connected
gs = G(INPUT_2);# assert gs.connected
gs.mode = 'GYRO-ANG'
original_angle = gs.angle
print("ANGLE:", original_angle)

btn = Button()

class G:
	def __init__(self):
		self.mode = 'hi'

def turn(timeturn, direc):
	"""
	Start both motors.
	`run-direct` allows varying motor performance on the fly
	by adjusting `duty_cycle_sp` attribute.
	"""
	#rightMotor.run_direct(duty_cycle_sp=99)
	#leftMotor.run_direct(duty_cycle_sp=-99)
	leftMotor.run_timed(speed_sp=-1*direc*1000, time_sp=timeturn*1000) #turning
	rightMotor.run_timed(speed_sp=direc*1000, time_sp=timeturn*1000)
	time.sleep(1)

#check around until us.distance() is close

# KEEP TURNING UNTIL GYROSCOPE IS AT CERTAIN ANGLE (ANGLE FOUND OTHER ROBOT*2)
# FOR ANGLES: BASE OFF TIME. LONGER == GREATER ANGLE
backspace_click = False

print("READY: ")
while not backspace_click:
	if btn.backspace:
		backspace_click = True
		time.sleep(2)

found = False

"""while True:
	sensorMotor.run_timed(speed_sp=500, time_sp=300)
	distance = us.value()
	print(distance)
	
	if distance < 300:
		# FOUND ROBOT
		print("ANGLE FOUND AT:", gs.angle)
		angle_found = gs.angle-original_angle
		print("DIFFERENCE:", gs.angle-original_angle)
		Sound.speak("FOUND").wait()
		sensorMotor.run_timed(speed_sp=-500, time_sp=300) #reverse
		time.sleep(0.1)
		break
	else:
		time.sleep(0.5)
		sensorMotor.run_timed(speed_sp=-500, time_sp=300)
		if distance < 300:
		# FOUND ROBOT
			print("ANGLE FOUND AT:", gs.angle)
			angle_found = gs.angle-original_angle
			print("DIFFERENCE:", gs.angle-original_angle)
			Sound.speak("FOUND").wait()
			sensorMotor.run_timed(speed_sp=500, time_sp=300) #reverse
			time.sleep(0.1)
			found = True
			break"""

timeBefore = time.time()
sensorMotor.run_timed(speed_sp=350, time_sp=1200)
# function this up
print("HEY")
while True:
	distance = us.value()
	print(distance)
	if distance < 300:
		timeAfter = time.time()
		timeDifference = timeAfter - timeBefore
		direction = 1
		sensorMotor.run_direct(duty_cycle_sp=0)
		print("ANGLE FOUND AT:", gs.angle)
		angle_found = gs.angle-original_angle
		print("DIFFERENCE:", gs.angle-original_angle)
		print("FOUND AFTER {} SECONDS".format(timeDifference))
		Sound.speak("f").wait()
		found = True
		break
	if (time.time() - timeBefore)*1000 > 1200:
		print("Nothing found")
		break
		# robot hasn't been found in this sweep


"""timeBefore = time.time()
if not found:
	sensorMotor.run_timed(speed_sp=-250, time_sp=1800)
	print("HI")
	while True:
		distance = us.value()
		print(distance)
		if distance < 300:
			timeAfter = time.time()
			timeDifference = timeAfter - timeBefore
			direction = -1 #reverse
			sensorMotor.run_direct(duty_cycle_sp=0)
			print("ANGLE FOUND AT:", gs.angle)
			angle_found = gs.angle-original_angle
			print("DIFFERENCE:", gs.angle-original_angle)
			print("FOUND AFTER {} SECONDS", timeDifference)
			Sound.speak("f").wait()
			found = True
			break"""


# then get angle and turn wheels there after the 3 seconds

if timeDifference > 0.6: # half way?
	direction = -1

time.sleep(0.1)
print(timeDifference)
#angle_found
input("Ready to turn?")
turn(timeDifference, direction)
##sensorMotor.run_direct(duty_cycle_sp=0)
#leftMotor.run_timed(speed_sp=1050, time_sp=1000) #turning
#rightMotor.run_timed(speed_sp=1050, time_sp=1000)




#rightMotor.stop()
#leftMotor.stop()