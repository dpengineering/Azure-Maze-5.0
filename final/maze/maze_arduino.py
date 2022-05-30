from final.imports.imports import * # import all useful from this path.


class Ball_Pump:
    def __init__(self):
        self.board = Arduino('/dev/ttyUSB0')  # /dev/ttyUSB0 = port of the Arduino nano
        with open("maze_arduino.txt", "r") as f: # before this class even runs, the coder must put the word 'right', or 'left' in maze_arduino.txt, if not already there.
            start_orientation = str(f.readline())
        self.orientation = start_orientation



    # def log_new_position(self): # old code that doesn't work
    #     with open("maze_arduino.txt", "r+") as f:
    #         if str(f.readline()) == "right":
    #             self.orientation = "left"
    #             f.truncate(0)
    #             f.write(str(self.orientation))
    #         elif str(f.readline()) == "left":
    #             self.orientation = "right"
    #             f.truncate(0)
    #             f.write(str(self.orientation))

    def pump(self): # pumps the opposite pump of what was previously done
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

    def change_pump(self, pump_num): # writing to arduino
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

    def start_left_pump(self): # simple command for left
        self.change_pump(1)

    def start_right_pump(self): # simple command for right
        self.change_pump(0)

    def stop_pumps(self): : # stops both pumps from pumping
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


if __name__ == '__main__': # testing for pumps, if not working as planned. run this file, and literally type anything for input, and pumps should pump alternating as you put new input.
    bp = Ball_Pump()
    while True:
        e = input("Enter which pump: ")
        bp.pump()

#if the arduinos still refuse to work, open the arduino IDE and upload/verify. also make sure that the right port is being connected to. open the serial monitor to see the print statements  and run python code. the print statements should work and change with what the python is telling arduno to do.
