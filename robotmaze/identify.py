def f():
	while ls.color != 5:
		rightMotor.run_direct(duty_cycle_sp=50)
		leftMotor.run_direct(duty_cycle_sp=50)
		import time; time.sleep(0.1)
	rightMotor.stop()
	leftMotor.stop()
	mot.run_direct(duty_cycle_sp=-50)
	time.sleep(5)
	mot.stop()
	rightMotor.run_direct(duty_cycle_sp=-100)
	leftMotor.run_direct(duty_cycle_sp=-100)