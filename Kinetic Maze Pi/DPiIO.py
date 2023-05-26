#      ******************************************************************
#      *                                                                *
#      *                   DPiClockNBlock Library                       *
#      *                                                                *
#      *            Arnav Wadhwa                   11/27/2022           *
#      *                                                                *
#      ******************************************************************

from dpeaDPi.DPiNetwork import DPiNetwork

dpiNetwork = DPiNetwork()

#
# DPiNetwork DPi_IO commands
#
_CMD_DPi_IO__PING                  = 0x00
_CMD_DPi_IO__INITIALIZE            = 0x01
_CMD_DPi_IO__DRIVER_ON             = 0x02
_CMD_DPi_IO__DRIVER_OFF            = 0x03
_CMD_DPi_IO__PULSE_DRIVER_ON       = 0x04
_CMD_DPi_IO__PULSE_DRIVER_OFF      = 0x05
_CMD_DPi_IO__SET_PWM_FREQUENCY     = 0x06
_CMD_DPi_IO__SET_DRIVER_PWM        = 0x07
_CMD_DPi_IO__READ_INPUT            = 0x10

#
# other constants used by this class
#
_NUMBER_OF_IO_INPUTS = 4
_DPiNETWORK_TIMEOUT_PERIOD_MS = 3
_DPiNETWORK_BASE_ADDRESS = 0x3C


class DPiIO:


    #
    # constructor for the DPiClockNBlock class
    #
    def __init__(self):
        #
        # attributes local to this class
        #
        self._slaveAddress = _DPiNETWORK_BASE_ADDRESS
        self._commErrorCount = 0

    # ---------------------------------------------------------------------------------
    #                                 Private functions
    # ---------------------------------------------------------------------------------

    #
    # send a command to the DPiSolenoid, command's additional data must have already been "Pushed".
    # After this function returns data from the device is retrieved by "Popping"
    #    Enter:  command = command byte
    #    Exit:   True returned on success, else False
    #
    def __sendCommand(self, command: int):
        (results, failedCount) = dpiNetwork.sendCommand(self._slaveAddress, command, _DPiNETWORK_TIMEOUT_PERIOD_MS)
        self._commErrorCount += failedCount
        return results

    # ---------------------------------------------------------------------------------
    #                                Public functions
    # ---------------------------------------------------------------------------------

    #
    # set the DPiSolenoid board number
    #    Enter:  boardNumber = DPiSolenoid board number (0 - 3)
    #
    def setBoardNumber(self, boardNumber: int):
        if (boardNumber < 0) or (boardNumber > 3):
            boardNumber = 0
        self._slaveAddress = _DPiNETWORK_BASE_ADDRESS + boardNumber

    #
    # ping the board
    #    Exit:   True returned on success, else False
    #
    def ping(self):
        return self.__sendCommand(_CMD_DPi_IO__PING)

    #
    # initialize the board to its "power on" configuration
    #    Exit:   True returned on success, else False
    #
    def initialize(self):
        return self.__sendCommand(_CMD_DPi_IO__INITIALIZE)

    #
    # get the count of communication errors
    #    Exit:   0 return if no errors, else count of errors returned
    #
    def getCommErrorCount(self):
        return self._commErrorCount

    #
    # Read an input
    #    Enter:  inputNumber = input number (0 - 3)
    #    Exit:   True, input value returned on success, else False, False
    #
    def readInput(self, inputNumber: int):
        if (inputNumber < 0) or (inputNumber >= _NUMBER_OF_IO_INPUTS):
            return False

        command = _CMD_DPi_IO__READ_INPUT + inputNumber
        if self.__sendCommand(command):
            return True, dpiNetwork.popUint8()
        else:
            return False, False

    #
    # Start pulsing the driver
    #   Exit: True on success, else False
    #
    def pulseDriver(self, enableFlg=False, blinkDurationMS=1000):

        if (blinkDurationMS < 1) or (blinkDurationMS > 65000):
            return False

        dpiNetwork.pushUint8(int(enableFlg))
        dpiNetwork.pushUint16(blinkDurationMS)
        return self.__sendCommand(_CMD_DPi_IO__PULSE_DRIVER_ON)

    #
    # Turn the driver on or off
    #   Exit: True on success, else False
    #
    def turnDriverOnOrOff(self, onOffValue=False):

        return self.__sendCommand(_CMD_DPi_IO__DRIVER_ON if onOffValue else _CMD_DPi_IO__DRIVER_OFF)

    #
    # Set the PWM frequency
    #   Enter: pwmFrequency = PWM cycles/second (100 to 100000)
    #   Exit: True on success, else False
    #
    def setPWMFrequency(self, pwmFrequency: int = 1000):
        if (pwmFrequency < 100) or (pwmFrequency > 100000):
            return False

        dpiNetwork.pushUint32(pwmFrequency)
        return self.__sendCommand(_CMD_DPi_IO__SET_PWM_FREQUENCY)

    #
    # set driver PWM
    #   Enter: pwmValue = 0 for off, 255 max on
    #   Exit: True on success, else False
    #
    def setDriverPWM(self, pwmValue: int = 0):
        if (pwmValue < 0) or (pwmValue > 255):
            return False

        dpiNetwork.pushUint8(pwmValue)
        return self.__sendCommand(_CMD_DPi_IO__SET_DRIVER_PWM)

