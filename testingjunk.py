# # import speech_recognition
# # import pyttsx3
from threading import Thread
import time
from time import sleep
# # recognizer = speechh_recognition.Recognizer()
# #
# # while True:
# #     try:
# #         with speech_recognition.Microphone() as mic:
# #             recognizer.adjust_for_ambient_noise(mic, duration=0.2)
# #             audio = recognizer.listen(mic)
# #
# #             text = recognizer.recognize_google(audio)
# #             text = text.lower()
# #             print(f"recognized {text}")
# #     except speech_recognition.UnknownValueError:
# #         print("not clear audio, please try again")
# #         # except Exception as e:
# #
# #         recognizer = speech_recognition.Recognizer()
# #         continue
# '''
# add thgis to class later om ,make the backend a true backend!
# '''
timer_time = 0
def start_timer():
    '''
    #starts a timer, this could break because of thread count, transfer to prox sensors
    '''
    Thread(target=start_timer_thread).start()

def reset_timer():
    global base_time
    base_time = time.time()
def start_timer_thread():
    global timer_time, base_time, current_time
    base_time = time.time()
    while True:
        current_time = time.time()
        timer_time = int(current_time - base_time)
        sleep(1)

def ret_time():
    global timer_time
    return timer_time

start_timer()

while True:
    print(ret_time())
    if timer_time == 4:
        reset_timer()




import cv2
import numpy as np
#
# # Make empty black image
# image = np.zeros((20, 40, 3), np.uint8)
# cv2.imwrite("before.png", image)
# # Make one pixel red
# image[10, 5] = [0, 0, 255]
#
# # Save
# cv2.imwrite("result.png", image)
