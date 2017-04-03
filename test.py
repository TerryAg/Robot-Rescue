def locate():
	initialTime = time()
	sensorMotor.run_to_rel_pos(position_sp=90, speed_sp=500)
	distance = 2550
	while distance > ROBOT_DISTANCE:
		distance = us.value()
		print(distance)
		if sensorMotor.position == 90: break
		if distance <= ROBOT_DISTANCE:
			endTIme = time()
			sensorMotor.stop()
			print(sensorMotor.position)
			return endTime-initialTime
	sensorMotor.run_to_rel_pos(position_sp=-180, speed_sp=500)
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
			return endTime-initialTime



def locate(DIRECTION):
	""" 
	Locates the other robot and returns how long it took to find it.

	After finding it, the UltrasonicSensor is reverted back to its initial position (0)
	"""
	initialTime = time()
	sensorMotor.run_to_abs_pos(position_sp=270, speed_sp=DIRECTION*BASE_MOTOR_SPEED) # rel_pos so it goes full cycle
	distance = 2550 # Don't make it us.value() in case while loop doesn't run
	while distance > ROBOT_DISTANCE:
		distance = us.value()
		print(distance)
		if distance <= ROBOT_DISTANCE: # FOUND 
			endTime = time()
			sensorMotor.stop()
			print(sensorMotor.position)
			if sensorMotor.position > 180: # NOT SURE IF WORKS
				DIRECTION = -1
			else:
				DIRECTION = 1
			sensorMotor.run_to_rel_pos(position=-25, speed_sp=DIRECTION*1000) #position=-25
			return ((endTime-initialTime)*3000, DIRECTION)