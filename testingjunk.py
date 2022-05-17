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

class Timer:
    def __init__(self):
        self.timer_time = 0
        self.base_time = None
        self.current_time = None

    def start_timer(self):
        Thread(target=self.start_timer_thread, daemon=True).start()

    def start_timer_thread(self):
        self.base_time = time.time()
        while True:
            self.current_time = time.time()
            self.timer_time = int(self.current_time - self.base_time)
            sleep(1)

    def reset_timer(self):
        self.base_time = time.time()

    def return_time(self):
        return self.timer_time

timer = Timer()
timer.start_timer()
while True:
    print(timer.return_time())
    sleep(1)
#
# timer_time = 0
# def start_timer():
#     '''
#     #starts a timer, this could break because of thread count, transfer to prox sensors
#     '''
#     Thread(target=start_timer_thread).start()
#
# def reset_timer():
#     global base_time
#     base_time = time.time()
# def start_timer_thread():
#     global timer_time, base_time, current_time
#     base_time = time.time()
#     while True:
#         current_time = time.time()
#         timer_time = int(current_time - base_time)
#         sleep(1)
#
# def return_time():
#     global timer_time
#     return timer_time
#
# start_timer()
#
# while True:
#     print(return_time())
#     if timer_time == 4:
#         reset_timer()




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
