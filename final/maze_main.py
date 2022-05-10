from imports import *
from maze_camera import *
from maze_arduino import *


if __name__ == '__main__':
    camera = Kinect()
    pumps = Ball_Pump("right")
    camera.start()

    try:
        camera.motor.ax.idle()
        while True:
            while not camera.motor.ball_enter_sensor_tripped:
                pumps.pump()
                sleep(3)
            sleep(6)
    finally:
        camera.motor.ax.idle()

