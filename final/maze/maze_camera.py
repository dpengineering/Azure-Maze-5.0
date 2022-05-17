from final.imports.imports import *

from maze_motor import OdriveMotor


class Kinect:

    def __init__(self):
        # Initialize the library, if the library is not found, add the library path as argument
        self.combined_image = None
        self.body_image_color = None
        self.depth_color_image = None
        self.body_frame = None
        self.capture = None
        # self.Kinect_Motor_Is_On = True
        self.Kinect_Is_On = True
        self.Keyboard_Is_On = False
        pykinect.initialize_libraries(module_k4abt_path="/usr/lib/libk4abt.so", track_body=True)
        self.device_config = pykinect.default_configuration
        self.device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
        self.device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        self.device = pykinect.start_device(config=self.device_config)
        self.bodyTracker = pykinect.start_body_tracker()
        self.close_body = None  # phase into closest centered body, reject left and right bounds
        self.motor = OdriveMotor("207C34975748", 15, 5)  # TODO: changed from 10 to 5 # why
        self.motor.kinect_motor_calibrate()
        self.motor.check_prox_constantly()
        self.time = 0

        self.start_sequence = False

    def start(self):
        Thread(target=self.start_thread, daemon=True).start()

    def time(self):
        return self.time

    def kinect_setup_image(self, showImage: bool = True):
        self.capture = self.device.update()

        self.body_frame = self.bodyTracker.update()

        ret, self.depth_color_image = self.capture.get_colored_depth_image()

        ret, self.body_image_color = self.body_frame.get_segmentation_image()
        if not ret:
            return

        self.combined_image = cv2.addWeighted(self.depth_color_image, 0.6, self.body_image_color, 0.4, 0)

        self.combined_image = self.body_frame.draw_bodies(self.combined_image)

        # resized = cv2.resize(combined_image, (1000, 1000))
        # fliparray
        self.combined_image = numpy.fliplr(self.combined_image)
        self.search_for_closest_body(self.body_frame)
        if showImage:
            cv2.imshow('Depth image with skeleton', self.combined_image)
        cv2.waitKey(1)

    def off(self):
        self.Kinect_Is_On = False

    def on(self):
        self.Kinect_Is_On = True

    def search_for_closest_body(self, frame):

        body_list = [frame.get_body_skeleton(body_num) for body_num in
                     range(frame.get_num_bodies())]  # creates bodylist
        try:
            self.close_body = min(body_list, key=lambda body: body.joints[
                26].position.xyz.z)  # grabs the minimum body according to the head z depth
        except ValueError:
            self.close_body = None

    def generate_points(self, joint: str):
        if self.close_body is not None:
            return self.close_body.joints[K4ABT_JOINT_NAMES.index(joint)].position.xyz

    def start_thread(self):
        cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
        print(self.motor.ball_enter_sensor_tripped, self.motor.ball_exit_sensor_tripped)
        while self.Kinect_Is_On:
            while self.motor.ball_enter_sensor_tripped:
                self.kinect_setup_image()
                # tested, works
                if self.close_body is not None:
                    # Added a min check to ensure velocity between -2 and 2
                    vel = float(int(self.generate_points("head").z)) / 1900  # changed back after presentation
                    # print(vel)
                    # vel = max(-2, min(2, float(int(self.generate_points("head").z)) / 1900))  # changed back after presentation

                    hand_left_y = self.generate_points("left hand").y
                    hand_right_y = self.generate_points("right hand").y
                    hand_right_x = self.generate_points("right hand").x
                    hand_left_x = self.generate_points("left hand").x
                    hand_slope = (hand_left_y - hand_right_y) / (hand_left_x - hand_right_x)

                    head_x = self.generate_points("head").x
                    head_y = self.generate_points("head").y

                    if head_y > hand_right_y and head_y > hand_left_y and hand_left_x-hand_right_x < 50:
                        self.start_sequence = True

                    if abs(vel) <= 2 and self.start_sequence:
                        if -0.2 < hand_slope < 0.2:
                            self.motor.ax.set_ramped_vel(-(self.motor.ax.get_vel()), int(1.2 * vel))
                        if hand_slope > 0.2:
                            self.motor.ax.set_vel(vel)
                        if hand_slope < -0.2:
                            self.motor.ax.set_vel(-vel)
                    if hand_right_x < -700 or hand_right_x > 700:
                        self.motor.ax.set_ramped_vel(0, 2)
                    if hand_left_x < -700 or hand_left_x > 700:
                        self.motor.ax.set_ramped_vel(0, 2)
                if self.motor.ball_exit_sensor_tripped:
                    print("exit")
                    self.motor.ax.idle()
                    self.motor.ball_enter_sensor_tripped = False
            while self.motor.ball_exit_sensor_tripped:
                self.kinect_setup_image()
                self.start_sequence = False
                if self.motor.ball_enter_sensor_tripped:
                    # print("entered")
                    self.motor.ball_exit_sensor_tripped = False

            sleep(0.1)
            # print('waiting...')


if __name__ == '__main__':
    k = Kinect()
    k.start()
    while True:
        try:
            sleep(10)
        finally:
            k.motor.ax.idle()

