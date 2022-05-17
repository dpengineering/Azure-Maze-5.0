# Ignore all of this


# from final.imports.imports import *
# from final.imports.kivy_imports import *
# from maze_camera import *
# from maze_arduino import *
# import os
#
# class test:
#
#     stop = ObjectProperty(None)
#     left = ObjectProperty(None)
#     right = ObjectProperty(None)
#
#     def start_game(self):
#         hand_left_y = camera.generate_points("left hand").y
#         print(hand_left_y)
#
# def start_thread():
#
#     try:
#         camera.start()
#         camera.motor.ax.idle()
#         while True:
#             while not camera.motor.ball_enter_sensor_tripped:
#                 pumps.pump()
#             #     sleep(3)
#             # sleep(6)
#     finally:
#         camera.motor.ax.idle()
#
# if __name__ == "__main__":
#     camera = Kinect()
#     pumps = Ball_Pump("right")
#     Thread(target=start_thread).start()
#
