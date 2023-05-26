from dpeaDPi.DPiStepper import DPiStepper
from dpeaDPi.DPiComputer import DPiComputer
from dpeaDPi.DPiPowerDrive import DPiPowerDrive
from time import sleep
from threading import Thread

from dpea_p2p.client import Client
import enum

dpiStepper = DPiStepper()
dpiComputer = DPiComputer()
dpiPowerDrive = DPiPowerDrive()

class PacketType(enum.Enum):
    COMMAND0 = 0
    COMMAND1 = 1
    COMMAND2 = 2
    COMMAND3 = 3
    COMMAND4 = 4
    COMMAND5 = 5
    COMMAND6 = 6


c = Client("172.17.21.1", 5001, PacketType)
c.connect()


class Main:
    def check(self):
        while True:
            Ball_Pump().switch()


class Ball_Pump:

    def __init__(self):
        # super(Ball_Pump, self).__init__(*args, **kwargs)
        # Thread(target=self.listen, daemon=True).start()

        dpiStepper.setBoardNumber(0)
        dpiStepper.initialize()
        dpiStepper.enableMotors(True)
        self.microstepping = 8
        self.speed_steps_per_second = 1000 * self.microstepping
        self.accel_steps_per_second_per_second = self.speed_steps_per_second
        self.steps = 1600
        self.wait_to_finish_moving_flg = True
        self.steps_per_rotation = 1600
        self.homeSpeedInStepsPerSecond = self.speed_steps_per_second
        self.homeMaxDistanceToMoveInSteps = 120000

        dpiComputer.initialize()
        dpiPowerDrive.initialize()
        dpiPowerDrive.setBoardNumber(0)

    def listen(self):
        global packetvalue, pack
        while True:
            pack = c.recv_packet()
            packetvalue = pack[1].decode()
            sleep(0.05)

    def quitting(self):
        if c.recv_packet() == (PacketType.COMMAND6, b'quit'):
            c.close_connection()
            quit()

    def left_sensor(self):
        if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0):
            sleep(1)
            print("Input 0 is HIGH")
            return True
        else:
            print("Input 0 is LOW")
            return False

    def right_sensor(self):
        if dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1):
            sleep(1)
            print("Input 1 is HIGH")
            return True
        else:
            print("Input 1 is LOW")
            return False

    def left_pump_home(self):
        stepper_num = 0
        stepper_status = dpiStepper.getStepperStatus(0)
        if stepper_status == (True, True, True, False):
            directionToMoveTowardHome = -1
            dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome,
                                         self.homeSpeedInStepsPerSecond, self.homeMaxDistanceToMoveInSteps)
        elif stepper_status == (True, True, True, True):
            print('Left pump is already homed.')
        else:
            print('ERROR: not homed; still moving; motors may not be enabled.')

    def right_pump_home(self):
        stepper_num = 1
        stepper_status = dpiStepper.getStepperStatus(1)
        if stepper_status == (True, True, True, False):
            directionToMoveTowardHome = 1
            dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome,
                                         self.homeSpeedInStepsPerSecond, self.homeMaxDistanceToMoveInSteps)
        elif stepper_status == (True, True, True, True):
            print('Right pump is already homed.')
        else:
            print('ERROR: not homed; still moving; motors may not be enabled.')

    def left_ball_pump(self):
        stepper_num = 0
        # stepper_status = dpiStepper.getStepperStatus(0)
        # if stepper_status == (True, True, True, True):
        #     dpiStepper.moveToRelativePositionInSteps(0, -3 * self.steps_per_rotation, self.wait_to_finish_moving_flg)
        # elif stepper_status == (True, True, True, False):
        # if self.left_sensor() == False:
        #     print("Needs ball. Will run right pump instead.")
        #     self.right_ball_pump()
        # elif self.left_sensor() == True:
        while True:
            if not self.left_sensor():
                print("Needs a ball.")
                sleep(3)
            elif self.left_sensor():
                dpiStepper.moveToRelativePositionInSteps(0, -3 * self.steps_per_rotation, self.wait_to_finish_moving_flg)
                directionToMoveTowardHome = -1
                dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome,
                                             self.homeSpeedInStepsPerSecond, self.homeMaxDistanceToMoveInSteps)
                sleep(1)
                break
        x = False
        count = 0
        while x:
            if self.left_sensor():
                sleep(1)
                x = True
                break
            elif not self.left_sensor():
                sleep(0.5)
                dpiStepper.moveToRelativePositionInSteps(0, -1 * self.steps_per_rotation,
                                                         self.wait_to_finish_moving_flg)
                count += 1
                x = False
                if count >= 2:
                    break

    def right_ball_pump(self):
        stepper_num = 1
        # if self.right_sensor() == False:
        #     print("Needs ball. Will run left pump instead.")
        #     self.left_ball_pump()
        # elif self.right_sensor() == True:
        while True:
            if not self.right_sensor():
                print("Needs a ball.")
                sleep(3)
            elif self.right_sensor():
                dpiStepper.moveToRelativePositionInSteps(1, 3 * self.steps_per_rotation, self.wait_to_finish_moving_flg)
                directionToMoveTowardHome = 1
                dpiStepper.moveToHomeInSteps(stepper_num, directionToMoveTowardHome,
                                             self.homeSpeedInStepsPerSecond, self.homeMaxDistanceToMoveInSteps)
                sleep(1)
                break
        x = False
        count = 0
        while x:
            if self.right_sensor():
                sleep(1)
                x = True
                break
            elif not self.right_sensor():
                sleep(0.5)
                dpiStepper.moveToRelativePositionInSteps(1, 1 * self.steps_per_rotation,
                                                         self.wait_to_finish_moving_flg)
                count += 1
                x = False
                if count >= 2:
                    break

    def piston_on(self):
        dpiPowerDrive.switchDriverOnOrOff(0, True)
        sleep(13)

    def piston_off(self):
        sleep(13)
        dpiPowerDrive.switchDriverOnOrOff(0, False)

    def switch(self):
        pack = c.recv_packet()
        packetType = str(pack[0])
        if packetType == "PacketType.COMMAND0":
            print('left ball pump')
            self.left_ball_pump()
        elif packetType == "PacketType.COMMAND1":
            print('right ball pump')
            self.right_ball_pump()
        elif packetType == "PacketType.COMMAND2":
            print('left home')
            self.left_pump_home()
        elif packetType == "PacketType.COMMAND3":
            print('right home')
            self.right_pump_home()
        elif packetType == "PacketType.COMMAND4":
            print('raising piston')
            self.piston_on()
        elif packetType == "PacketType.COMMAND5":
            print('lowering piston')
            self.piston_off()
        elif packetType == "PacketType.COMMAND6":
            print('quitting')
            self.quitting()



if __name__ == "__main__":
    Main().check()
