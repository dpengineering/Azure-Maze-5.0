import threading # for threading.active_count(), which returns the total number of active threads at that given time.

from final.imports.imports import * # import everything else

from maze_motor import OdriveMotor # import OdriveMotor class from maze_motor.py, as the Kinect class contains a built in instance of that class called 'motor'.


class Kinect:

    def __init__(self):
        # Initialize the library, if the library is not found, add the library path as argument
        self.combined_image = None # frame that is being displayed by cv2
        self.body_image_color = None # other part of frame that is being layered with cv2 'addweighted'
        self.depth_color_image = None
        self.body_frame = None
        self.capture = None
        
        self.motor_is_on = True # setup for start (in thread), the most important function is what it calls, start_thread()
        self.kinect_is_on = True # always on, but can have the option for being turned off.
        #setup stuff
        pykinect.initialize_libraries(module_k4abt_path="/usr/lib/libk4abt.so", track_body=True)
        self.device_config = pykinect.default_configuration
        self.device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
        self.device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        self.device = pykinect.start_device(config=self.device_config)
        self.bodyTracker = pykinect.start_body_tracker()
        # self.close_body is really valuable, as this is the bread and butter of this code. it finds not only the closest body, but the closest body that is centered, which means that the camera will always obey the closest centered person, no matter how large or positioned the crowd is.
        self.close_body = None  # phase into closest centered body, reject left and right bounds
        self.motor = OdriveMotor("207C34975748", 15, 5)  # serial number, current_lim, velocity lim. motor will error out if the latter two are breached. 
        self.time = 0 # not used

        self.movement_text = "" # used to write to the displayed camera frame what the user is doing.

        self.summon_ball = False # used to trigger on and off the ball pump arduinos in main and main_keyboardless.
        # keyboard, has parallels with https://github.com/nikhi1g/blind_keyboard that should be helpful
        self.key_left = False
        self.key_right = False
        self.row_top = False
        self.row_middle = False
        self.row_bottom = False
        self.row_enter = False
        self.clicked = False
        self.delete = False

    def start(self):
        Thread(target=self.start_thread, daemon=True).start() # thread to start

    def time(self):
        return self.time

    def kinect_setup_image(self, showImage: bool = True): # creates one frame and displays that frame to a window called 'depth image with skeleton'
        self.capture = self.device.update()

        self.body_frame = self.bodyTracker.update()

        ret, self.depth_color_image = self.capture.get_colored_depth_image()

        ret, self.body_image_color = self.body_frame.get_segmentation_image()
        if not ret:
            return

        self.combined_image = cv2.addWeighted(self.depth_color_image, 0.6, self.body_image_color, 0.4, 0)

        self.combined_image = self.body_frame.draw_bodies(self.combined_image)

        self.combined_image = numpy.fliplr(self.combined_image)
        # self.search_for_closest_body(self.body_frame)
        self.findClosestCenteredIndex()
        # new
        self.combined_image = cv2.cvtColor(self.combined_image, cv2.COLOR_BGR2RGB) # convert combined image to a writeable format.

        self.combined_image = cv2.putText(self.combined_image, self.movement_text, (50, 50),
                                          cv2.FONT_HERSHEY_SIMPLEX,
                                          1, (255, 0, 0), 2, cv2.LINE_AA)

        if showImage: # option to display image in function itself set default to be true.
            cv2.imshow('Depth image with skeleton', self.combined_image)
        cv2.waitKey(1)

    def findClosestCenteredIndex(
            self):  # Expected return: Index of closest body, their head's x value, their head's y value, more advanced and better than search_for_closest_body
        head_x_values = []
        head_z_values = []
        for body_index in range(self.body_frame.get_num_bodies()): # loops through each recognized body
            body_skel = self.body_frame.get_body_skeleton(body_index)
            head_x = abs(body_skel.joints[K4ABT_JOINT_NAMES.index("head")].position.xyz.x)
            head_x_values.append(head_x)
            head_z = body_skel.joints[K4ABT_JOINT_NAMES.index("head")].position.xyz.z
            head_z_values.append(head_z)
        for body_index in range(self.body_frame.get_num_bodies()):
            if head_z_values[body_index] > 4500: # rejects anyone 4.5 m away from camera.
                head_x_values[body_index] = 10000
        if len(head_x_values) > 0:
            closest_body_skel = self.body_frame.get_body_skeleton(head_x_values.index(min(head_x_values))) # finds the most centered body that is closest - 95
            head_depth_z = closest_body_skel.joints[K4ABT_JOINT_NAMES.index("head")].position.xyz.z
            joint_names = ["nose", "right shoulder", "left shoulder", "left knee", "right knee"]
            joints_out_of_bounds = [closest_body_skel.joints[K4ABT_JOINT_NAMES.index(name)].position.xyz.x == 0 for name
                                    in joint_names]
            if any(joints_out_of_bounds):
                self.close_body = None
            else:
                self.close_body = closest_body_skel
        else:
            self.close_body = None

    def search_for_closest_body(self, frame): # phased out, function above works better.

        body_list = [frame.get_body_skeleton(body_num) for body_num in
                     range(frame.get_num_bodies())]  # creates bodylist
        try:
            self.close_body = min(body_list, key=lambda body: body.joints[
                26].position.xyz.z)  # grabs the minimum body according to the head z depth
        except ValueError:
            self.close_body = None

    def generate_points(self, joint: str): # allows for user to generate points based on string value associated with index, see file K4ABT_JOINT_NAMES, just command click on that in the code
        if self.close_body is not None:
            return self.close_body.joints[K4ABT_JOINT_NAMES.index(joint)].position.xyz

    def type_on_frame(self, text: str): # not used, types on frame
        self.combined_image = cv2.cvtColor(self.combined_image, cv2.COLOR_BGR2RGB)

        self.combined_image = cv2.putText(self.combined_image, text, (50,50),
                                          cv2.FONT_HERSHEY_SIMPLEX,
                                          1, (255, 0, 0), 2, cv2.LINE_AA)

    def home_maze(self): # finds where the proxmity sensor hits the screw on the back and then turns to home.
        # self.motor.ax.set_pos_traj(-3.11, 0.3, 2, 1) # cheap shortcut that doesn't actually work properly each time
        self.motor.home_maze()
        sleep(1)
        while self.motor.ax.is_busy(): # this will actually trigger teh watchdog, so the camera output will freeze until one second after the maze is homed.
            sleep(1)

    def start_thread(self):
        cv2.namedWindow('Depth image with skeleton', cv2.WINDOW_NORMAL)
        while self.kinect_is_on:
            while self.motor_is_on:

                self.kinect_setup_image() # sets up one frame

                # print(self.motor.ax.get_vel())
                # so as I understand it, this is how the watchdog works: it receives data, and is happy (does nothing). when it doesn't get input, 
                # it throws an error.
                if abs(self.motor.ax.get_vel()) <= 2.5: # will throw watchdog error, because watchdog is not being fed data when vel > 2.5.
                    # https://docs.odriverobotics.com/v/latest/getting-started.html?highlight=watchdog#watchdog-timer
                    self.motor.ax.axis.watchdog_feed()

                if self.close_body is not None: # if there is a recognized person.

                    if not self.motor.ax.axis.config.enable_watchdog: # if self.motor.ax.axis.config.enable_watchdog == False:
                        self.motor.ax.axis.error = 0 # clear the error
                        self.motor.ax.axis.config.enable_watchdog = True # reenable the watchdog

                    vel = float(int(self.generate_points("head").z)) / 1900 # scales the velocity based on how close or far the person is away from the Kinect.
                    # generate relevant points
                    hand_left_y = self.generate_points("left hand").y
                    hand_right_y = self.generate_points("right hand").y
                    hand_right_x = self.generate_points("right hand").x
                    hand_left_x = self.generate_points("left hand").x
                    hand_right_z = self.generate_points("right hand").z
                    hand_left_z = self.generate_points("left hand").z

                    head_x = self.generate_points("head").x
                    head_y = self.generate_points("head").y
                    head_z = self.generate_points("head").z

                    hand_slope = (hand_left_y - hand_right_y) / (hand_left_x - hand_right_x)

                    head_x = self.generate_points("head").x
                    head_y = self.generate_points("head").y
                    head_x_adjusted = head_x + 1000
                    # 2000
                    #keyboardstuff
                    if 0 < head_x_adjusted < 600:  # right side
                        self.row_bottom = True
                    if 660 < head_x_adjusted < 1260:  # middle side
                        self.row_middle = True
                    if 1320 < head_x_adjusted < 1920:  # left side
                        self.row_top = True
                    if hand_slope > 0.2:  # key left
                        self.key_left = True
                    if hand_slope < -0.2:  # key right
                        self.key_right = True
                    if hand_left_z > head_z and hand_right_z > head_z:
                        self.delete = True
                    #end keyboardstuff
                    # if abs(hand_slope) < 0.2 and head_y > hand_right_y + 100 and head_y > hand_left_y + 100:
                    #     self.row_enter = True # disabled permanently, moved to pumps' summon_ball

                    if hand_left_y < (head_y + 100) and hand_left_y > (head_y - 100) and hand_left_x < (
                            head_x + 100) and hand_left_x > (head_x - 100) or hand_right_y < (
                            head_y + 100) and hand_right_y > (head_y - 100) and hand_right_x < (
                            head_x + 100) and hand_right_x > (head_x - 100): # behold the best if statement you will ever see :D Basically self.clicked will be set to true if the person covers their eyes.
                        self.clicked = True
                    if abs(hand_slope) < 0.2 and head_y > hand_right_y + 10 and head_y > hand_left_y + 10: # raise both hands with relatively flat slope above head
                        self.summon_ball = True
                    # if head_y > hand_right_y and head_y > hand_left_y and hand_left_x - hand_right_x < 50:  # clap above head, pretty hard to do, changed to code directly above.
                    #     self.summon_ball = True

                    if self.motor.ball_enter_sensor_tripped: # if a ball has entered.
                        # print("entered")
                        if -0.2 < hand_slope < 0.2: # stops the motor with negative of current velocity if hand slope is relatively flat, which allows for better braking and accounts for some momentum of the wheel
                            self.movement_text = "stopping"
                            self.motor.ax.set_vel(-(self.motor.ax.get_vel()))
                        if abs(vel) <= 2 and self.summon_ball: # making extra sure that the user only can move the maze between vel -2 and 2.
                            if hand_slope > 0.2:  # left
                                self.movement_text = "lefting" # changes movement text, which is called in function kinect_setup_image()
                                self.motor.ax.set_vel(vel)

                            if hand_slope < -0.2:  # right
                                self.motor.ax.set_vel(-vel)
                                self.movement_text = "righting" # changes movement text called in kinect_setup_image()

                        if hand_right_x < -700 or hand_right_x > 700: # stops motor if user out of bounds
                            self.motor.ax.set_ramped_vel(0, 2)
                        if hand_left_x < -700 or hand_left_x > 700: # stops motor if user out of bounds
                            self.motor.ax.set_ramped_vel(0, 2)
                else:

                    sleep(self.motor.watchdog_sleep + 0.5)  # greater than or equal to watchdog sleep
                    # watchdog will not be fed when user completes the maze
                    self.motor.ax.axis.config.enable_watchdog = False
                if self.motor.ball_exit_sensor_tripped:
                    print("exit")
                    self.movement_text = "please wait for maze to home"
                    self.motor.is_homed = False # reloads variable
                    self.summon_ball = False # reloads variable
                    self.motor.ax.axis.error = 0
                    self.motor.ax.axis.config.enable_watchdog = False
                    self.home_maze() # homes 
                    self.motor.ax.idle()
                    sleep(1)
                    self.movement_text = "ready!"
                    self.motor.is_homed = True # sets is_homed to true
                    # reset switches
                    self.motor.ball_enter_sensor_tripped = False
                    self.motor.ball_exit_sensor_tripped = False


if __name__ == '__main__': # run this for debugging the class.
    k = Kinect() # creates instance of Kinect class
    k.start() # starts kinect
    while True:
        try:
            sleep(10) # you actually need the main 'thread' to be busy, as k.start() is a thread and will execute as daemon = True. if you take this out and put like print("hello world") or something the project won't work.
        finally:
            k.motor.ax.idle() # stop the motor.
