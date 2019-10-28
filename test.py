from ev3dev2.motor import LargeMotor, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_A, OUTPUT_C, MediumMotor, OUTPUT_D

l_speed = 500
r_speed = 50

print(l_speed, r_speed)

left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_D)

left_motor.stop()
right_motor.stop()

left_motor.run_timed(speed_sp=l_speed, time_sp=3000)
right_motor.run_timed(speed_sp=r_speed, time_sp=3000)