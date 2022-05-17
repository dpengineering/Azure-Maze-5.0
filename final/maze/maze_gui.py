from final.imports.imports import *
from final.imports.kivy_imports import *
from maze_camera import *
from maze_arduino import *
from maze_timer import *
import os

SCREEN_MANAGER = ScreenManager()
START_SCREEN_NAME = 'Start_Screen'
PLAY_SCREEN_NAME = 'Play_Screen'


class KinectGUI(App):
    def build(self):
        # StartScreen.enter_thread()
        return SCREEN_MANAGER


# create screen without kinect and other stuff

Window.clearcolor = (0, 0, 0, .01)  # Black


class StartScreen(Screen):
    clap = ObjectProperty(None)
    welcome_text = ObjectProperty(None)

    def enter(self):
        Thread(target=self.enter_thread, daemon=True).start()


    # @staticmethod
    def enter_thread(self):
        while True:
            try:
                if camera_is_ready and camera.start_sequence:
                    print("Switching to play screen")
                    # self.clap.trigger_action(0.1)
                    break
            except NameError:
                pass

    #
    # while True:
    #     if switch_to_play_screen:
    #         # TODO murder thread
    #         print("Switch")

    # TODO Can't Switch Screens with a thread, apparently, yay thanks :D

    def switch_to_play_screen(self):
        SCREEN_MANAGER.current = PLAY_SCREEN_NAME


class PlayScreen(Screen):

    def enter(self):
        print("entered")


Builder.load_file('Screens/StartScreen.kv')
Builder.load_file('Screens/PlayScreen.kv')
SCREEN_MANAGER.add_widget(StartScreen(name=START_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PlayScreen(name=PLAY_SCREEN_NAME))


def start_thread():
    global camera_is_ready
    try:

        camera.start()
        camera.motor.ax.idle()
        camera_is_ready = True
        while True:
            while not camera.motor.ball_enter_sensor_tripped:
                # pumps.pump()
                # sleep(3)
                sleep(1)
            sleep(6)
    finally:
        camera.motor.ax.idle()


if __name__ == "__main__":
    camera_is_ready = False
    camera = Kinect()

    pumps = Ball_Pump("right")
    sleep(3)
    Thread(target=start_thread, daemon=True).start()
    KinectGUI().run()
