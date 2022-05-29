# Azure-Maze-5.0
Kinetic Maze with Azure Kinect and Python Library

Note that this is a Dos Pueblos Engineering Academy project, and it is assumed that this project is running with DPEA pre-configured hardware/software, specifically [RaspberryPiCommon](https://github.com/dpengineering/RaspberryPiCommon), and associated engineering packages. You have probably learned about this already.



## Installation ##
***This is already done on the 'Tuf Gaming' Computer, situated under the circuitry in the Kinetic Maze. Skip this step if this is you.***

Instructions to install the Azure Kinect SDK are from microsoft, copied here for convinience.

1. Configure the Microsoft Package Repository, and install the Azure Kinect packages (tools, headers, and body tracking):
```
 curl -sSLhttps://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
 sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
 sudo apt-get update
 sudo apt install k4a-tools
 sudo apt install libk4a1.4-dev
 sudo apt install libk4abt1.1-dev
```
Note: requires OpenGL 4.4 and above, use ```sudo apt install nvidia-driver-455``` to install proper video card driver.

If your device is not being properly recognized by ```k4aviewer``` you may need to set the usb device rules.
To properly set usb device rules:

```
cd /etc/udev/rules.d && sudo wget https://raw.githubusercontent.com/microsoft/Azure-Kinect-Sensor-SDK/develop/scripts/99-k4a.rules
```

To check that your Kinect is properly recognized, run
```
AzureKinectFirmwareTool -q
```


## Azure Kinect on Linux ##
As most Microsoft documentation is windows based, Linux usage will be documented as thoroughly as possible for future use. In general, follow instructions in the Microsoft documentation.

To launch the Azure Kinect Viewer, run `k4aviewer` in the command line. A window will pop up from the terminal. Hit 'start' to verify that the camera is working.

## How to Run ##

To start the project, clone this repo or download directly.
Navigate to final/imports and open all three files.
Make sure that all the imported packages are downloaded correctly. Make sure to keep kivy specific imports seperate from the other packages, as it will try to open up a starter window automatically if you import kivy_imports.py along with imports.py and ODrive_Ease_Lib.py.

Great! Now head over to final/maze/main_keyboardless.py and run that file. Head over to the back of the project and disconnect the motor from interacting with the wheel. The odrive will start to calibrate. Wait until it finishes calibrating - it will start to spin in only one direction, which means that it is homing. TODO: set Odrive to precalibrated `odrv0.axis0.motor.config.pre_calibrated`.




## Reference Links ##
[Azure Kinect Samples](https://github.com/microsoft/Azure-Kinect-Samples)

[Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)

[Azure Kinect DK Documentation](https://docs.microsoft.com/en-us/azure/kinect-dk/)

[Body Tracking SDK Reference](https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.x.x/index.html)

[Azure Kinect Sensor SDK Reference](https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html)
