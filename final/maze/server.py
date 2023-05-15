from final.imports.imports import *
import enum

class PacketType(enum.Enum):
    COMMAND0 = 0
    COMMAND1 = 1
    COMMAND2 = 2
    COMMAND3 = 3
    COMMAND4 = 4
    COMMAND5 = 5


s = Server("172.17.21.2", 5001, PacketType)
serverCreated = False


def create_server():
    global serverCreated
    print('server created')
    s.open_server()
    print('server opened, now waiting for connection!')
    s.wait_for_connection()
    serverCreated = True
    return True


def pump(num):
    if num == 0:
        if serverCreated is True:
            s.send_packet(PacketType.COMMAND0, b"left pump")
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