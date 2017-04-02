from ev3dev.ev3 import *
import time

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
sensorMotor = Motor(OUTPUT_C)
us = UltrasonicSensor(INPUT_1); assert us.connected
btn = Button()


# Global variables
sumoDistance = 300 # Distance between our robot and their robot
sensorDirection = 1

def startup():
	"""A function which detects whether the backspace button is pressed.

	Used for determining when to start the actual sumo robot."""
	backspace_click = False
	print("READY: ")
	while not backspace_click:
		if btn.backspace:
			backspace_click = True
			time.sleep(3)
			return backspace_click

def locate(sensorDirection, delay=0, secondtime=0):# Need to change this to have an in-built delay
	initialTime = time.time() if secondtime == 0 else secondtime
	found = False
	sensorTime = 1200
	sensorMotor.run_timed(speed_sp=sensorDirection*350, time_sp=sensorTime)
	sensorDirection = -1 if sensorDirection == 1 else 1
	# can sensorMotor use duty_cycle_sp? if so use it. then sensorTime isn't needed
	while True: # Change this to have an actual condition, simlar to drive()
		distance = us.value()
		#print(distance)
		timePassed = time.time()
		timeDifference = timePassed - initialTime
		if distance < sumoDistance:
			sensorMotor.stop(stop_action='brake') # Stop motor
			# PROBLEM: Motor goes a little bit more even after finding
			found = True
			print("FOUND AFTER {} SECONDS".format(timeDifference))
			#Sound.speak("f")
			if timeDifference > 0.6: # More than half way
				timeDifference = 1.2 - timeDifference
				motorDirection = -1
			else:
				motorDirection = 1
			break
		if timeDifference*1000 > sensorTime and not found:
			print("NOTHING FOUND")
			#input("nothing found")
			return locate(sensorDirection, secondtime=time.time()) # Backtrack

	time.sleep(delay)
	#input('turn sensor back to orig')
	sensorMotor.run_timed(speed_sp=sensorDirection*350, time_sp=timeDifference*1000)
	#input('did it turn correctly?')
	return timeDifference, motorDirection
	# Reset sensor to beginning


def turn(turningTime, motorDirection):
	turningTime *= 1300
	leftMotor.run_timed(speed_sp=motorDirection*1000, time_sp=turningTime)
	rightMotor.run_timed(speed_sp=-1*motorDirection*1000, time_sp=turningTime)
	time.sleep(1)


def drive():
	while us.value() < sumoDistance:
		leftMotor.run_direct(duty_cycle_sp=100)
		rightMotor.run_direct(duty_cycle_sp=100)
		# in lecture today he did time.sleep(0.1) while using duty_cycle_sp
		time.sleep(0.1)
	 # Out of range of other robot -- WILL NEED CHANGING
	timeTaken, motorDirection = locate(sensorDirection) # NO DELAY.
	# WILL THERE BE NAME CLASHES WITH SENSORDIRECTION WHEN LOCATE IS CALLED
	# MULTIPLE TIMES?
	turn(timeTaken, motorDirection) # Directions for sensor/motor might need changes
	

		# if touch sensor touched: keep pushing, ignore other methods.
	# Touch sensor?


def main():
	"""Main function of the program."""
	timeTaken, motorDirection = locate(sensorDirection, delay=3) # Won't exactly be 3... change.
	print("TIME DIFFERENCE:", timeTaken)
	turn(timeTaken, motorDirection)
	while True:
		try:
			drive()
		except Exception as e:
			print(e)
			leftMotor.run_direct(duty_cycle_sp=0)
			rightMotor.run_direct(duty_cycle_sp=0) # There is a way to stop other than this right?

if __name__ == '__main__':
	startup()
	main()



# duty_cycle_sp means percentage of how much power