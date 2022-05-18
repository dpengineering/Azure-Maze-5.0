from final.imports.imports import *

class OdriveMotor:
    def __init__(self, odrive_serial_number = "207C34975748", current_limit=15, velocity_limit=5):
        self.serial_number = odrive_serial_number
        self.current_limit = current_limit
        self.velocity_limit = velocity_limit
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

        self.kinect_motor_calibrate()
        self.check_switches_constantly()



    def home_maze(self):
        # self.ax.home_with_endstops(vel=0.1)
        velocity = 2
        self.ax.set_vel(2)
        while True:
            if int(bin(self.odrive_board.get_gpio_states())[-7]) == 0:
                self.ax.set_home()
                break
        self.ax.set_ramped_vel(0, 2)
        while self.ax.is_busy():
            sleep(1)

        self.ax.set_pos_traj(-3.4, 1, 2, 1) # pos, accel, deaccel, home
        sleep(1)
        while self.ax.is_busy():
            sleep(1)


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
    kinect_motor = OdriveMotor()
    try:

        sleep(1)
        kinect_motor.home_maze()
        # kinect_motor.kinect_motor_calibrate()
        # sleep(1)
        # kinect_motor.ax.set_vel(1)

    finally:
        dump_errors(kinect_motor.odrive_board)
        sleep(6)
        kinect_motor.ax.idle()