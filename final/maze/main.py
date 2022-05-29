import threading

from final.imports.kivy_imports import *
from final.maze.maze_camera import *
from final.maze.maze_arduino import *

camera = Kinect() # creates Kinect object as instance camera from maze_camera
pumps = Ball_Pump()# creates ball pump object as instance pumps from maze_arduino
SCREEN_MANAGER = ScreenManager() # allows one to switch screens, and is constantly being returned in the MazeGUI class.
START_SCREEN_NAME = 'start' # this should look familiar. If not check ouout the starter code inside https://github.com/dpengineering/RaspberryPiCommon/tree/master/PiKivyProjects/NewProject
PLAY_SCREEN_NAME = 'play'
TYPE_SCREEN_NAME = 'type'
LEADERBOARD_SCREEN_NAME = 'leader'




class MazeGUI(App):
    def build(self):
        return SCREEN_MANAGER


Window.clearcolor = (0, 0, 0, 1)  # sets window color to black


class StartScreen(Screen):

    clap = ObjectProperty(None) # referenced from StartScreen.kv

    def enter(self):  # this function is called when the StartScreen.kv is loaded.
        print(f"Thread Count {threading.active_count()}")  # threading.active_count is very useful, as it returns the number of active threads. think of a thread like a worker that the main project spawsn, which can do work while other things are executing.
        # camera.motor.home_maze()  # don't need this
        # camera.motor.ax.set_pos_traj(-3.11, 0.3, 2, 1)  # don't need this, but set_pos_traj goes to a pos at an acceleration, target velocity, and deacceleration. Kind of like an airplane.
        Thread(target=self.enter_thread, daemon=True).start()

    def enter_thread(self): # a thread, what this does it allows the user to summon a ball.
        while True:
            try:
                sleep(0.01)
                if camera.summon_ball:
                    print('summoning ball')
                    pumps.pump() # pumps left of right pump based on the input rewritten in maze_arduino.txt
                    sleep(4) #was2  # waits a bit
                    Clock.schedule_once(self.transition)  # calls the transition function. Clock.schedule_once(func, dt) is a great way of executing functions outside a thread, from inside a thread.
                    break
            except NameError:
                pass # this try/except can probably be removed as the camera object fully loads now.
        print("Exiting Start Thread")

    def transition(self, dt):
        SCREEN_MANAGER.current = PLAY_SCREEN_NAME  # changes the output screen to PLAY_SCREEN_NAME, which is loaded at the bottom of the file, and referenced next.


class PlayScreen(Screen):
    timer_button = ObjectProperty(None)  # the timer button has an attribute called text, which is updated frequently in the while loop.

    def enter(self):
        self.timer_button.text = ""  # clear from previous loop of project
        Thread(target=self.timer, daemon=True).start()  # thread

    def timer(self):
        global score  # global a score variable so that it can be called later and prevents miswrites which affects leaderboard scoring
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
            c_time = time.time() 
            score = int(c_time - base_time)
            score = str(score)
            sleep(1)
            self.timer_button.text = score
            if camera.motor.ball_exit_sensor_tripped:
                Clock.schedule_once(self.transition)
                break

    def transition(self, dt):
        SCREEN_MANAGER.current = LEADERBOARD_SCREEN_NAME


class TypeScreen(Screen):  # keyboardscreen, which does not work at the moment, but should allow input for name.
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

    def keyboard_movement(self):  # failed :(
        while True:
            print(camera.row_middle)
            camera.row_middle = False
            if SCREEN_MANAGER.current != TYPE_SCREEN_NAME:
                break
            sleep(0.25)

    def set_keyboard_keys(self):  # if you need a keyboard, this is a great code snippet to copy along with the rest of the kivy stuff.
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
            self.transition()
        else:
            self.nickname.text = "Not A Name!"

    def transition(self):
        SCREEN_MANAGER.current = LEADERBOARD_SCREEN_NAME

class LeaderboardScreen(Screen):  # sorts any file into a leaderboard that has the format: score, name, newline
    leaderboard = ObjectProperty(None)
    leaderboard_greeting = ObjectProperty(None)

    def enter(self):
        self.score_update()

    def score_update(self):
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
        # self.leaderboard.text = ""
        # self.leaderboard_greeting.text = "Thank you\nfor playing!"


    def transition(self, dt):
        SCREEN_MANAGER.current = START_SCREEN_NAME
 
 #loads each of the files needed from Screens.
Builder.load_file('Screens/StartScreen.kv') 
Builder.load_file('Screens/PlayScreen.kv')
Builder.load_file('Screens/TypeScreen.kv')
Builder.load_file('Screens/LeaderboardScreen.kv')
SCREEN_MANAGER.add_widget(StartScreen(name=START_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PlayScreen(name=PLAY_SCREEN_NAME))
SCREEN_MANAGER.add_widget(TypeScreen(name=TYPE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(LeaderboardScreen(name=LEADERBOARD_SCREEN_NAME))


if __name__ == "__main__":
    camera.start()  # calls instance of Kinect to execute start function. only works because this in of itself calls a thread
    camera.motor.ax.idle()  # frees the motor, so that it doesn't burn up? or is that loop control...?
    MazeGUI().run()  # runs the gui
