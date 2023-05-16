import numpy
from datetime import datetime
import os
import cv2
import pyautogui
import sys
# from kivy.uix.button import Button
# Email stuff
# import KineticMail
from pykinect_azure.k4abt._k4abtTypes import K4ABT_JOINT_NAMES
from pykinect_azure.k4abt import _k4abt
import pykinect_azure as pykinect
from pykinect_azure.k4a import _k4a
from final.imports.ODrive_Ease_Lib import *
from time import sleep
# uiStuff
import datetime
import random
from pyautogui import *
import time
# from kivy.properties import ObjectProperty
# from kivy.app import App
# from kivy.core.window import Window, Animation
# from kivy.lang import Builder
# from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.graphics.texture import Texture
from threading import Thread
# from kivy.clock import Clock
from time import sleep
# from Email import Email
# from Firmata import Firmata
from pyfirmata import Arduino, util



import numpy as np
import cv2


# from kivy.graphics.texture import Texture
# from kivy.clock import Clock
# from kivy.uix.image import Image
# from pidev.kivy import DPEAButton
# from pidev.kivy import ImageButton
# # from datetime import datetime #not working, set date for may 30th, 2022 reminder if emails do work
# from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
# from pidev.MixPanel import MixPanel