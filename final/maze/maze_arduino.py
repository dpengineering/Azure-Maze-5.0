from final.imports.imports import *


class Ball_Pump:
    def __init__(self, start_orientation):
        self.board = Arduino('/dev/ttyUSB0')  # /dev/ttyUSB0 = port of the Arduino nano
        self.orientation = start_orientation

    def pump(self):
        if self.orientation == "left":
            self.pump_left_once()
            # print("left pump")
            self.orientation = "right"
        elif self.orientation == "right":
            self.pump_right_once()
            # print("right pump")
            self.orientation = "left"

    def change_pump(self, pump_num):
        """
            0 for right, 1 for left
        """
        if pump_num == 1:
            self.board.digital[4].write(1)
            self.board.digital[3].write(0)
            pump_num = 0
            # print(f"pumping left pump {pump_num}")

        elif pump_num == 0:
            self.board.digital[4].write(0)
            self.board.digital[3].write(1)
            pump_num = 1
            # print(f"pumping right pump {pump_num}")

    def start_left_pump(self):
        self.change_pump(1)

    def start_right_pump(self):
        self.change_pump(0)

    def stop_pumps(self):
        self.board.digital[4].write(0)
        self.board.digital[3].write(0)

    def pump_left_once(self):
        self.start_left_pump()
        sleep(1)
        self.stop_pumps()

    def pump_right_once(self):
        self.start_right_pump()
        sleep(1)
        self.stop_pumps()
