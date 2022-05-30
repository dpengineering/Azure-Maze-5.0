# Azure-Maze-5.0
**Kinetic Maze with Azure Kinect and Python Library [IMPORTANT](https://github.com/ibaiGorordo/pyKinectAzure)
**


Note that this is a Dos Pueblos Engineering Academy project, and it is assumed that this project is running with DPEA pre-configured hardware/software, specifically [RaspberryPiCommon](https://github.com/dpengineering/RaspberryPiCommon), and associated engineering packages. You have probably learned about this already, but just in case. Github Dark Dimmed theme for the win!

I highly recommend 'blind coding', or prepping tidbits or entire sections of code that don't need the project's hardware to run, and then adding them directly to the project. You don't need classes for this to work, as seen in [Azure-Maze-2.0](https://github.com/dpengineering/Azure-Maze-2.0), but they are really helpful. The first version of this project can be found [here](https://github.com/dpengineering/azure-maze).

Q: What happened to 3.0 and 4.0?

A: They're there on the Tuf Gaming computer in the undercarriage of the maze. Note that in there may be some code pertaining to the Mirrored Light Sculpture on there (or maybe it's on another computer...?), but please don't lose those!

**please read the rest of this readme, you may have to do some steps if you aren't using the 'Tuf Gaming' computer, but take note that all specific documentation is located in the [`documentation`](https://github.com/dpengineering/Azure-Maze-5.0/tree/documentation) branch of this project. Just click on any file and there will be comments next to each line (save for imports).**

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

As most Microsoft documentation is windows based, Linux usage will be documented as thoroughly as possible for future use. In general, follow instructions in the Microsoft documentation.

To launch the Azure Kinect Viewer, run `k4aviewer` in the command line. A window will pop up from the terminal. Hit 'start' to verify that the camera is working.

## How to Run ##

To start the project, clone this repo or download directly.
Navigate to final/imports and open all three files.
Make sure that all the imported packages are downloaded correctly. Make sure to keep kivy specific imports seperate from the other packages, as it will try to open up a starter window automatically if you import kivy_imports.py along with imports.py and ODrive_Ease_Lib.py.

Great! Now head over to final/maze/main_keyboardless.py and run that file. Head over to the back of the project and disconnect the motor from interacting with the wheel. The odrive will start to calibrate. Wait until it finishes calibrating - it will start to spin in only one direction, which means that it is homing, and you can set it down. **If you don't do this step properly you will get error CONTROLLER_ERROR_SPINOUT_DETECTED when you dump errors of odboard, and will have to troubleshoot.**

Now sit back and wait for TWO windows to pop up, and then left justify the camera output screen and right justify the kivy screen. Copy the images on the screen to work the project.

How the project works currently: 

Joints: x,y,z, measured in mm from the lens of the camera.

It calculates the slope (like you learned in math class) between your left and right hands. Based on whether the slope is positive, negative, or close to flat, the Odrive will spin the wheel clockwise, counterclockwise, or stop. 
The motor currently brakes by setting its current velocity to negative what the encoder reads. This allows the wheel to stop with some momentum included - it is more responsive this way.

File Structure: 


final: contains the classes, text storage, and kivy files.


final/imports: contains all the imports that were used for the project, and serves as a good way of organizing code.

final/maze: code for all the classes, UI, and main files that run the project.


final/maze/Screens: houses each kivy screen that is used in both final/maze/main.py and final/maze//main_keyboardless.py

final/maze/leaderboard.txt: houses the leaderboard, which on working properly allows people to enter in their name, which it does, just not hands free 

from final/maze/main.py. 

final/maze/maze_arduino.txt: stores the last direction pumped, so that the project never gets unevenly stacked with the pool balls.


main.py: runs through each screen of Screens, currently is bugged. some useful code for an emulated keyboard, [here](https://github.com/nikhi1g/blind_keyboard).

**main_keyboardless.py:** runs without keyboard or leaderboard, and runs very smoothly. there is only one issue with the Arduino sometimes not working when the user wants it to pump a ball.


the **classes** housed in final that are used are in maze_arduino.py, maze_camera.py, and maze_motor.py. maze_timer.py works, but is not used.

**_Note: all classes have testing in the if __name__ == "__main__": part, so if something is not working, try to run these files individually_**

maze_arduino.py: connects to the arduino upon initialization and controls the pumps.

maze_camera.py: controls the camera (Kinect), and an instance of the class in maze_motor.py

maze_motor.py: controls the motor (Odrive), and also checks for proximity sensors. Make sure that when you move the motor you only have that movement in one part of your code. Controlling the motor from two threads will throw an unfixable error, and the fix is just to not do that (learned that the hard way).

Arduino: Backup storage for the arduino code. 

pyKinectAzure: [IMPORTANT](https://github.com/ibaiGorordo/pyKinectAzure) library that actually allows us to use the Kinect.

testingjunk.py: coding scratchpad for ideas. was currently working on speech-to-text to enter names and the now successful timer class.



TODO: set Odrive to precalibrated `odrv0.axis0.motor.config.pre_calibrated`.

TODO: make one beautiful, 'full-screen' version of the project that has the camera output built into it, instead of a separate window. 
Look into [Gantry Game GUI](https://github.com/dpengineering/GantryGame3.0/blob/Main/Picasso_Bot_Gui.py) and the original [Picasso Bot GUI](https://github.com/nikhi1g/Picasso_Bot_Gui/blob/main/Picasso_Bot_Gui.py), and of course Google!

TODO: add a current 'position' image to the kivy PlayScreen.kv and main_keyboardless.py where it displays the action figure of what the person is doing. You can accomplish this with self.movement_text, or directly from hand_slope with linked variables.



## Reference Links ##
[Azure Kinect Samples](https://github.com/microsoft/Azure-Kinect-Samples)

[Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)

[Azure Kinect DK Documentation](https://docs.microsoft.com/en-us/azure/kinect-dk/)

[Body Tracking SDK Reference](https://microsoft.github.io/Azure-Kinect-Body-Tracking/release/1.x.x/index.html)

[Azure Kinect Sensor SDK Reference](https://microsoft.github.io/Azure-Kinect-Sensor-SDK/master/index.html)


## Farewell ##
Looking back, and when you look at the project, it may not even make sense at all. You may want to give up, or leave out features because they are 'too hard'. If it is, and not essential, then move on but take not. Otherwise, keep chipping away at the problem until it collapses. I wish the best for you to work on this project and in future years to come. You may not need any level of documentation for code to work; if you understand it, and you may think, great!, I'm done! And push. NO. Please, please, please make sure that if it is **not** clear, you **explain** your code. In the comments. In the commit message. In a text file. Whatever works. If it is clear, that is a sign that you are programming better and better. As you expand on whatever code it is you work on, you will forget why you kept that variable a couple of weeks back, or will delete an 'irrelevent' part of the code that actually is necessary for things to work. Knowing why you did something, and continuing to know why will save you so much time in the future. You will also be able to get help from Mr.Harlow or Cesar or whoever else is there more effectively. Collaborate with your peers. Bounce ideas off of them. Give ideas. It's an idea economy over there in P1. Voice your ideas and hone them down so that you can draw what your project wil literally do. Don't be afraid to ask for help, but at the same time make sure you aren't a pushover with your bugs and errors, because then you will never learn. But, above all else, look forward to sitting down, tuning out the world, and just coding, writing. Testing, debugging, and finding success. 

If you are thinking about the project while in the shower, or while driving in the car, or while working out, or while eating, or doing anything else, you are doing something right. 

Before you rewrite, understand. Before you delete, understand why. Organization and functionality should be your top priorities; but, of the two, functionality matters 10 times more, so don't care about organization until you have something that works, or if it will make functionality work better.

Establish a 'your area'. Seperate from everyone else, or with a partner or two. Your area is optimized for you. Move stuff, make space, get that good chair, that keyboard and mouse. Keep it clean and neat. No distractions. Music is good if it helps you concentrate. If you have nothing else to do and you're working on a project that is being machined, fixed, or reworked, find something to do. Ask Harlow what you can do. Ask machine shop. Ask a friend about their project, you'll learn something. There is always stuff to do. 

At the end of the day, it is what you make of it. You can literally do almost nothing if you try to. But don't! It's your senior year, and you've come a long way. Establish and maintain trust. Joke, and laugh. Type so much that your fingertips hurt. Have respect for everyone, but don't care about that if it gets in the way helping someone. If you learn html or css and want to take it futher, make your own website using github. See [mine](https://nikhi1g.github.io/)! Make it fun! See egg puns on the one and only [thedailyegg!](https://thedailyegg.github.io/)

**If you have any questions about the maze or the code or whatever please contact me at `805 455 5199`. If I don't pick up, text "Azure-Maze" to me along with your question so you don't get blocked. Email is 2nikhil@gmail.com**
