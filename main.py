from ev3dev.ev3 import *
import time

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C)
us = UltrasonicSensor(INPUT_1); assert us.connected

btn = Button()

def startup():
	backspace_click = False
	print("READY: ")
	while not backspace_click:
		if btn.backspace:
			backspace_click = True
			time.sleep(2)
			return backspace_click

def locate(sensorDirection):
	initialTime = time.time()
	sensorTime = 1200
	sensorMotor.run_timed(speed_sp=sensorDirection*350, time_sp=sensorTime)
	while True:
		distance = us.value()
		print(distance)
		timePassed = time.time()
		timeDifference = timePassed - initialTime
		if distance < 300:
			sensorMotor.run_direct(duty_cycle_sp=0) # Stop motor
			# PROBLEM: Motor goes a little bit more even after finding
			print("FOUND AFTER {} SECONDS".format(timeDifference))
			Sound.speak("f").wait()
			return timeDifference

		if timeDifference*1000 > sensorTime:
			print("NOTHING FOUND")
			sensorDirection = -1 if sensorDirection == 1 else 1
			return locate(sensorDirection) # Backtrack

def turn(turningTime, motorDirection):
	turningTime *= 1300
	leftMotor.run_timed(speed_sp=motorDirection*1000, time_sp=turningTime)
	rightMotor.run_timed(speed_sp=-1*motorDirection*1000, time_sp=turningTime)
	time.sleep(1)

def drive():
	leftMotor.run_timed(speed_sp=1050, time_sp=5000)
	rightMotor.run_timed(speed_sp=1050, time_sp=5000)
	time.sleep(5) # Enough time to charge other robot out. If not, then we re-locate?
	# Touch sensor?

def main():
	timeTaken = locate(sensorDirection)
	if timeTaken > 0.6:
		timeTaken = 1.2 - timeTaken
		motorDirection = -1
	else:
		motorDirection = 1
	print("TIME DIFFERENCE:", timeTaken)
	turn(timeTaken, motorDirection)
	drive()


time.sleep(0.1)

if __name__ == '__main__':
	sensorDirection = 1
	startup(); assert backspace_click
	main()