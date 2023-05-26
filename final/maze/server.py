from final.imports.imports import *
from dpea_p2p.server import Server
import enum


class PacketType(enum.Enum):
    COMMAND0 = 0
    COMMAND1 = 1
    COMMAND2 = 2
    COMMAND3 = 3
    COMMAND4 = 4
    COMMAND5 = 5
    COMMAND6 = 6


s = Server("172.17.21.1", 5001, PacketType)
serverCreated = False


# def create_server():
#     global serverCreated
#     print('server created')
#     s.open_server()
#     print('server opened, now waiting for connection!')
#     s.wait_for_connection()
#     serverCreated = True
#     return True


class Ball_Pump:

    def __init__(self):
        with open("maze_arduino.txt", "r") as f:
            start_orientation = str(f.readline())
        self.orientation = start_orientation

    def create_server(self):
        global serverCreated
        print('server created')
        s.open_server()
        print('server opened, now waiting for connection!')
        s.wait_for_connection()
        serverCreated = True
        return True

    def check_server(self):
        if serverCreated == True:
            s.send_packet(PacketType.COMMAND6, b"quitting")
            s.close_connection()
            s.close_server()
        if serverCreated == False:
            self.create_server()


    def switch(self, num):
        if num == 0:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND0, b"left pump")
                # assert s.recv_packet() == (PacketType.COMMAND0, b"left pump")
        elif num == 1:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND1, b"right pump")
        elif num == 2:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND2, b"left home")
        elif num == 3:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND3, b"right home")
        elif num == 4:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND4, b"piston on")
        elif num == 5:
            if serverCreated is True:
                s.send_packet(PacketType.COMMAND5, b"piston off")

    def pump_left(self):
        self.switch(0)
        # assert s.recv_packet() == (PacketType.COMMAND0, b"left pump")

    def pump_right(self):
        self.switch(1)
        # assert s.recv_packet() == (PacketType.COMMAND1, b"right pump")

    def left_home(self):
        self.switch(2)
        # assert s.recv_packet() == (PacketType.COMMAND2, b"left home")

    def right_home(self):
        self.switch(3)
        # assert s.recv_packet() == (PacketType.COMMAND3, b"right home")

    def piston_on(self):
        self.switch(4)
        # assert s.recv_packet() == (PacketType.COMMAND4, b"piston on")

    def piston_off(self):
        self.switch(5)
        # assert s.recv_packet() == (PacketType.COMMAND5, b"piston off")

    def change_pumps(self, pump_num):
        if pump_num == 1:
            self.pump_right()
        elif pump_num == 0:
            self.pump_left()

    def pump_left_once(self):
        self.change_pumps(0)
        return True

    def pump_right_once(self):
        self.change_pumps(1)
        return True

    def pump(self):
        if self.orientation == "left":
            self.pump_left()
            with open("maze_arduino.txt", "w") as f:
                f.truncate(0)
                f.write("right")
            self.orientation = "right"
        elif self.orientation == "right":
            self.pump_right()
            with open("maze_arduino.txt", "w") as f:
                f.truncate(0)
                f.write("left")
            self.orientation = "left"


if __name__ == '__main__':
    server = Ball_Pump()
    while True:
        e = input("Enter which pump: ")
        server.pump()
