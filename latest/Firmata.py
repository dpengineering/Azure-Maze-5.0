from pyfirmata import Arduino, util
from time import sleep

board = Arduino('/dev/ttyUSB0')  # /dev/ttyUSB0 = port of the Arduino nano


class Firmata:

    def change_pump(self, xcv):
        if xcv == 1:
            board.digital[4].write(1)
            board.digital[3].write(0)
            xcv = 0
            print(xcv)

        elif xcv == 0:
            board.digital[4].write(0)
            board.digital[3].write(1)
            xcv = 1
            print(xcv)

    def turn_off(self):
        board.digital[4].write(0)
        board.digital[3].write(0)


#`
# What is with my luck in having things break on me?