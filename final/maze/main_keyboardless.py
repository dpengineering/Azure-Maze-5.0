 # this is the version of the project that should loop endlessly, and works until the arduinos don't pump for some weird reason.

import threading  # for active_count, for some reason isn't imported regularly
from final.imports.kivy_imports import *
from final.maze.maze_camera import *
from final.maze.maze_arduino import *

camera = Kinect() # instance of Kinect class, has instance of Odrive built in, as well as prox sensor and switches, which are GPIO
pumps = Ball_Pump() # instance of Ball_Pump class, which allows for control of ball pumps
SCREEN_MANAGER = ScreenManager()  # allows us to control the screen
START_SCREEN_NAME = 'start'  # loaded at bottom, allows for shortcut to call
PLAY_SCREEN_NAME = 'play'
TYPE_SCREEN_NAME = 'type'
LEADERBOARD_SCREEN_NAME = 'leader'




class MazeGUI(App):  # always returns what the SCREEN_MANAGER is
    def build(self):
        return SCREEN_MANAGER


Window.clearcolor = (0, 0, 0, 1)  # black, sets the window color


class StartScreen(Screen):
    clap = ObjectProperty(None)   # clap: clap in StartScreen.py connects kivy object to python.
    def enter(self):
        print(f"Thread Count {threading.active_count()}")
        Thread(target=self.enter_thread, daemon=True).start()

    def enter_thread(self):
        while True:
            try:
                sleep(0.01)
                if camera.summon_ball: # summon ball variable which is found in the Kinect() class
                    print('summoning ball')
                    pumps.pump()  # allows to pump alternate pumps, regardless of program shutdowns and physical project errors like ball getting stuck.
                    sleep(4) # sleep a bit before doing anything else, to make sure pumps move
                    Clock.schedule_once(self.transition)  # allows you to break out the the thread into the main kivy things to execute switch screen cleanly.
                    break
            except NameError:
                pass
        print("Exiting Start Thread")

    def transition(self, dt):
        SCREEN_MANAGER.current = PLAY_SCREEN_NAME  # switch screen


class PlayScreen(Screen):  # starts a timer and allows user to control the motor until the exit sensor is tripped.
    timer_button = ObjectProperty(None)
    def enter(self):
        self.timer_button.text = ""
        Thread(target=self.timer, daemon=True).start()
#revert toyes commit
    def timer(self): # simple timer
        global score
        self.timer_button.text = "Ready"
        time.sleep(7)
        self.timer_button.text = "Three"
        time.sleep(1)
        self.timer_button.text = "Two"
        time.sleep(1)
        self.timer_button.text = "One"
        time.sleep(1)
        self.timer_button.text = "Go!!!"
        time.sleep(1.3)
        base_time = time.time()
        while True:
            # restart to here
            print(self.movement_text.text)
            c_time = time.time()
            score = int(c_time - base_time)
            score = str(score)
            sleep(1) # was 1, change back if lag or error
            self.timer_button.text = score
            if camera.motor.ball_exit_sensor_tripped:
                Clock.schedule_once(self.transition)
                break

    def transition(self, dt):
        SCREEN_MANAGER.current = LEADERBOARD_SCREEN_NAME # skips TypeScreen haha


class TypeScreen(Screen): # keyboard, with associated objects and functions. doesn't get called anywhere as main_keyboardless.py is without keyboard.
    a1 = ObjectProperty(None)
    b1 = ObjectProperty(None)
    c1 = ObjectProperty(None)
    d1 = ObjectProperty(None)
    e1 = ObjectProperty(None)
    f1 = ObjectProperty(None)
    g1 = ObjectProperty(None)
    h1 = ObjectProperty(None)
    i1 = ObjectProperty(None)
    j1 = ObjectProperty(None)
    k1 = ObjectProperty(None)
    l1 = ObjectProperty(None)
    m1 = ObjectProperty(None)
    n1 = ObjectProperty(None)
    o1 = ObjectProperty(None)
    p1 = ObjectProperty(None)
    q1 = ObjectProperty(None)
    r1 = ObjectProperty(None)
    s1 = ObjectProperty(None)
    t1 = ObjectProperty(None)
    u1 = ObjectProperty(None)
    v1 = ObjectProperty(None)
    w1 = ObjectProperty(None)
    x1 = ObjectProperty(None)
    y1 = ObjectProperty(None)
    z1 = ObjectProperty(None)
    space = ObjectProperty(None)
    star = ObjectProperty(None)
    dash = ObjectProperty(None)
    delete = ObjectProperty(None)
    enterKey = ObjectProperty(None)
    nickname = ObjectProperty(None)

    def enter(self):
        self.set_keyboard_keys()
        Thread(target=self.keyboard_movement, daemon=True).start()

    def keyboard_movement(self):
        while True:
            print(camera.row_middle)
            camera.row_middle = False
            if SCREEN_MANAGER.current != TYPE_SCREEN_NAME:
                break
            sleep(0.25)

    def set_keyboard_keys(self): # you may want to copy just this class and test it somewhere else as it is very clean in of itself as a standalone keyboard.
        KeyboardObjectList = [self.q1, self.w1, self.e1, self.r1, self.t1, self.y1, self.u1, self.i1, self.o1, self.p1,
                              self.a1, self.s1, self.d1, self.f1, self.g1, self.h1, self.j1, self.k1, self.l1,
                              self.space,
                              self.z1, self.x1, self.c1, self.v1, self.b1, self.n1, self.m1, self.star, self.dash,
                              self.delete, self.enterKey]
        x_spacing = .1
        y_spacing = -.15
        x_offset = 0
        y_offset = 0
        button_count = 0
        for btn in KeyboardObjectList:

            btn.pos_hint = {"x": .02 + x_offset, "y": .55 + y_offset}
            button_count += 1
            x_offset += x_spacing
            btn.color = "lightblue"
            if button_count % 10 == 0:
                x_offset = 0
                y_offset += y_spacing

        self.enterKey.pos_hint = {"x": 0.1, "y": .1}
        self.nickname.color = "lightblue"
        self.nickname.text = "Enter Your Name:"

    def Key_Update(self, button):
        if ":" in self.nickname.text or "!" in self.nickname.text:
            self.nickname.text = ""
        self.nickname.text += button.text

    def Delete_Key_Update(self):
        if len(self.nickname.text) > 0:
            self.nickname.text = self.nickname.text[:-1]

    def Enter_Key_Update(self):
        if len(self.nickname.text) >= 1 and ":" not in self.nickname.text:
            with open("leaderboard.txt", "a") as f:
                f.write(score + " ")
                f.write(self.nickname.text + "\n")
            self.transition() # could also do Clock.schedule_one(self.transition, 1) and make transition() of transition(self, dt)
        else:
            self.nickname.text = "Not A Name!"

    def transition(self):
        SCREEN_MANAGER.current = LEADERBOARD_SCREEN_NAME

class LeaderboardScreen(Screen): # not actually a real leaderboard, just says thanks for playing and loops back to the start after some seconds.
    leaderboard = ObjectProperty(None)
    leaderboard_greeting = ObjectProperty(None)

    def enter(self):
        self.score_update()

    def score_update(self): # reads the text file left and right columns by score, name, and then sorts them to one string.
        scores = []
        names = []
        with open("leaderboard.txt", "r") as file:
            for line in file:
                split_line = line.strip().split()
                scores.append(split_line[0])
                names.append(split_line[1])

        pairs = list(zip(scores, names))
        pairs.sort(key=lambda pair: int(pair[0]))
        count = 1
        score_board = ""
        with open("leaderboard.txt", "r") as f:
            leader_length = len(f.readlines())

        while count < leader_length and count <= 10:
            score_board += str(count) + ".        " + pairs[count][0] + " " + pairs[count][1] + "\n"
            count += 1

        self.leaderboard.text = score_board
        Clock.schedule_once(self.transition, 5)
        # that took way too long
        self.leaderboard.text = ""
        self.leaderboard_greeting.text = "Thank you\nfor playing!"


    def transition(self, dt):
        SCREEN_MANAGER.current = START_SCREEN_NAME

 #loads all of the files and makes sure that the SCREEN_MANAgER is aware of them
Builder.load_file('Screens/StartScreen.kv') 
Builder.load_file('Screens/PlayScreen.kv')
Builder.load_file('Screens/TypeScreen.kv')
Builder.load_file('Screens/LeaderboardScreen.kv')
SCREEN_MANAGER.add_widget(StartScreen(name=START_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PlayScreen(name=PLAY_SCREEN_NAME))
SCREEN_MANAGER.add_widget(TypeScreen(name=TYPE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(LeaderboardScreen(name=LEADERBOARD_SCREEN_NAME))


if __name__ == "__main__":
    camera.start()
    camera.motor.ax.idle()
    MazeGUI().run()
