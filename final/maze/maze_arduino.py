from final.imports.imports import *


class Ball_Pump:
    def __init__(self):
        self.board = Arduino('/dev/ttyUSB0')  # /dev/ttyUSB0 = port of the Arduino nano
        with open("maze_arduino.txt", "r") as f:
            start_orientation = str(f.readline())
        self.orientation = start_orientation

    # def log_new_position(self):
    #     with open("maze_arduino.txt", "r+") as f:
    #         if str(f.readline()) == "right":
    #             self.orientation = "left"
    #             f.truncate(0)
    #             f.write(str(self.orientation))
    #         elif str(f.readline()) == "left":
    #             self.orientation = "right"
    #             f.truncate(0)
    #             f.write(str(self.orientation))

    def pump(self):
        if self.orientation == "left":
            self.pump_left_once()
            with open("maze_arduino.txt", "w") as f:
                f.truncate(0)
                f.write("right")
            self.orientation = "right"
        elif self.orientation == "right":
            self.pump_right_once()
            with open("maze_arduino.txt", "w") as f:
                f.truncate(0)
                f.write("left")
            self.orientation = "left"

    def pump_left(self):
        x = True
        while x:
            self.pump_left_once()
            sleep(3)

    def change_pump(self, pump_num):
        """
            0 for right, 1 for left
        """
        if pump_num == 1:
            self.board.digital[4].write(1)
            self.board.digital[3].write(0)
            # pump_num = 0
            # print(f"pumping left pump {pump_num}")

        elif pump_num == 0:
            self.board.digital[4].write(0)
            self.board.digital[3].write(1)
            # pump_num = 1
            # print(f"pumping right pump {pump_num}")

    def start_left_pump(self):
        self.change_pump(1)
        # self.board.digital[4].write(1)
        # self.board.digital[3].write(0)

    def start_right_pump(self):
        self.change_pump(0)
        # self.board.digital[4].write(0)
        # self.board.digital[3].write(1)

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

    def piston_on(self):
        self.board.digital[10].write(1)

    def piston_off(self):
        self.board.digital[10].write(0)


if __name__ == '__main__':
    bp = Ball_Pump()
    while True:
        e = input("Enter which pump: ")
        bp.pump()

#if no work, connect to serial id with arudinmo app opem