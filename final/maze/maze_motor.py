from final.imports.imports import *

class OdriveMotor:
    def __init__(self, odrive_serial_number = "207C34975748", current_limit=15, velocity_limit=7):
        self.serial_number = odrive_serial_number
        self.current_limit = current_limit
        self.velocity_limit = velocity_limit
        self.is_homed = False
        self.watchdog_sleep = 0.5
        self.odrive_board = odrive.find_any(serial_number=self.serial_number)
        self.ax = ODrive_Axis(self.odrive_board.axis0, self.current_limit, self.velocity_limit)
        self.ax.axis.config.enable_watchdog = False
        self.ax.axis.error = 0
        self.ax.axis.config.watchdog_timeout = self.watchdog_sleep
        self.homing_sensor = -7
        self.ball_enter_sensor = -9
        self.ball_exit_sensor = -8
        self.homing_sensor_tripped = False
        self.ball_enter_sensor_tripped = False
        self.ball_exit_sensor_tripped = False
        self.ax.clear_errors()
        self.kinect_motor_calibrate()
        self.check_switches_constantly()
        self.home_maze()

        # dump_errors(self.odrive_board)



    def home_maze(self):
        # self.ax.home_with_endstops(vel=0.1)
        # velocity = 2
        self.ax.set_vel(1)
        while True:
            if int(bin(self.odrive_board.get_gpio_states())[-7]) == 0:
                self.ax.set_home()
                break
        self.ax.set_ramped_vel(0, 2)
        while self.ax.is_busy():
            sleep(1)

        self.ax.set_pos_traj(-3.115, 0.3, 2, 1) # pos, accel, deaccel, home
        sleep(1)
        while self.ax.is_busy():
            sleep(1)

        self.is_homed = True
        print('homed')



    def kinect_motor_calibrate(self):
        if not self.ax.is_calibrated():
            print("calibrating wheel ... ")
            self.ax.calibrate()
            self.ax.gainz(20, 0.16, 0.32, False)
            self.ax.idle()
            dump_errors(self.odrive_board)

    def check_sensors(self):
        states = bin(self.odrive_board.get_gpio_states())
        if int(states[self.homing_sensor]) == 0:
            self.homing_sensor_tripped = True

        if int(states[self.ball_exit_sensor]) == 0:
            self.ball_exit_sensor_tripped = True
            self.ball_enter_sensor_tripped = False

        if int(states[self.ball_enter_sensor]) == 0:
            self.ball_enter_sensor_tripped = True
            self.ball_exit_sensor_tripped = False

    def check_switches_constantly(self):
        Thread(target=self.check_constantly_thread, daemon=True).start()

    def check_constantly_thread(self):
        print("checking switches constantly")
        self.ball_exit_sensor_tripped, self.ball_enter_sensor_tripped, self.homing_sensor_tripped = False, False, False
        while True:
            self.check_sensors()


if __name__ == '__main__':
    sleep(3)
    kinect_motor = OdriveMotor(odrive_serial_number = "207C34975748", current_limit=20, velocity_limit=8)
    try:
        # kinect_motor.ax.set_vel(2)
        kinect_motor.home_maze()

    finally:
        kinect_motor.ax.idle()
        dump_errors(kinect_motor.odrive_board)
    # try:
    #     kinect_motor.ax.set_vel(2)
    #     sleep(12)
    # finally:
    #     kinect_motor.ax.idle()
    #     print("idled")
    # try:
    #     print("before sleep")
    #     sleep(1)
    #     # kinect_motor.home_maze()
    #     # kinect_motor.kinect_motor_calibrate()
    #     # sleep(1)
    #     kinect_motor.ax.set_vel(1)
    #     sleep(10)
    # finally:
    #     dump_errors(kinect_motor.odrive_board)
    #     # sleep(6)
    #     kinect_motor.ax.idle()



'''
search path to fix CONTROLLER_ERROR_SPINOUT_DETECTED or MOTOR VOLTAGE ATTACHED
also change velocity limit, increase it probably
this is because encoder (or something) spins out of control for a fraction of a second,
and this trips whatever catch it has, but then returns to normal almost instantaneously
moral of the story, use looser limits (vel limit, current limit)
odrv0.axis0.motor.config.current_control_bandwidth = INCREASE IF CONTROLLER_ERROR_SPINOUT_DETECTED
https://discourse.odriverobotics.com/t/spinout-on-hoverboard-motors/7645
https://changelogs.md/github/madcowswe/odrive/
https://discourse.odriverobotics.com/t/encoder-error-cpr-polepairs-mismatch/5765
https://discourse.odriverobotics.com/t/encoder-seems-to-work-but-error-cpr-out-of-range-on-offset-calibration/1929/3
https://docs.odriverobotics.com/v/latest/control-modes.html
https://discourse.odriverobotics.com/t/multiple-errors-when-during-trap-moves-with-high-accelerations/7512/3
https://github.com/LuSeKa/HoverBot/blob/master/tools/ODrive_hoverboard_motor_setup_part_01.py
'''