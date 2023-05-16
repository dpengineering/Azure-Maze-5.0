import threading

from final.imports.kivy_imports import *
from final.maze.maze_camera import *
from final.maze.maze_arduino import *
from final.maze.server import *

camera = Kinect()
# pumps = Ball_Pump()
server = Server()

SCREEN_MANAGER = ScreenManager()
START_SCREEN_NAME = 'start'
PLAY_SCREEN_NAME = 'play'
TYPE_SCREEN_NAME = 'type'
LEADERBOARD_SCREEN_NAME = 'leader'




class MazeGUI(App):
    def build(self):
        return SCREEN_MANAGER


Window.clearcolor = (0, 0, 0, 1)  # black


class StartScreen(Screen):

    clap = ObjectProperty(None)

    def enter(self):
        print(f"Thread Count {threading.active_count()}")
        # camera.motor.home_maze()
        # camera.motor.ax.set_pos_traj(-3.11, 0.3, 2, 1)
        Thread(target=self.enter_thread, daemon=True).start()

    def enter_thread(self):
        while True:
            try:
                sleep(0.01)
                if camera.summon_ball:
                    print('summoning ball')
                    server.pump()
                    sleep(4) #was2
                    Clock.schedule_once(self.transition)
                    break
            except NameError:
                pass
        print("Exiting Start Thread")

    def transition(self, dt):
        SCREEN_MANAGER.current = PLAY_SCREEN_NAME


class PlayScreen(Screen):
    timer_button = ObjectProperty(None)

    def enter(self):
        self.timer_button.text = ""
        Thread(target=self.timer, daemon=True).start()

    def timer(self):
        global score
        self.timer_button.text = "Ready?"
        time.sleep(3)
        self.timer_button.text = "3"
        time.sleep(1)
        self.timer_button.text = "2"
        time.sleep(1)
        self.timer_button.text = "1"
        time.sleep(1)
        self.timer_button.text = "Go!"
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
        SCREEN_MANAGER.current = TYPE_SCREEN_NAME




class TypeScreen(Screen):
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
    bar = ObjectProperty(None)
    cursor = ObjectProperty(None)

    cursor_y_top_row = 0.54
    cursor_y_middle_row = 0.39
    cursor_y_bottom_row = 0.24
    cursor_size_hint = 0.05*1.3, 0.06

    top_row_pos_hint = {"x": .015, "y": .54}
    middle_row_pos_hint = {"x": .015, "y": .39}
    bottom_row_pos_hint = {"x": .015, "y": .24}

    bar_size_hint = 0.944, .06

    enter_key_pos_hint = {"x": .087, "y": .09}
    enter_size_hint = 0.09, .06

    # KeyboardObjectList = [q1, w1, e1, r1, t1, y1, u1, i1, o1, p1, a1, s1, d1, f1, g1, h1, j1, k1, l1,
    #                       space, z1, x1, c1, v1, b1, n1, m1, star, dash,
    #                       delete, enterKey]

    def enter(self):
        self.set_keyboard_keys()
        Thread(target=self.keyboard_movement, daemon=True).start()

        # self.cursor.pos_hint['y'] = self.t1.pos_hint['y'] - 0.01  # accurate per key, doesnt work in thread?
#0.0085
    def keyboard_movement(self):
        # top_row_buttons = [self.q1, self.w1, self.e1, self.r1, self.t1, self.y1, self.u1, self.i1, self.o1, self.p1]
        # middle_row_buttons = [self.a1, self.s1, self.d1, self.f1, self.g1, self.h1, self.j1, self.k1, self.l1, self.space]
        # bottom_row_buttons = [self.z1, self.x1, self.c1, self.v1, self.b1, self.n1, self.m1, self.star, self.dash, self.delete]
        # rows = [top_row_buttons,middle_row_buttons,bottom_row_buttons]
        # self.cursor.pos_hint['x'] = self.y1.pos_hint["x"] - 0.0085
        KeyboardObjectList = [self.a1, self.b1, self.c1, self.d1, self.e1, self.f1, self.g1, self.h1, self.i1, self.j1,
                              self.k1, self.l1, self.m1, self.n1, self.o1, self.p1, self.q1, self.r1, self.s1, self.space,
                              self.t1, self.u1, self.v1, self.w1, self.x1, self.y1, self.z1, self.star, self.dash, self.delete]
        # while SCREEN_MANAGER.current == TYPE_SCREEN_NAME:
        index = 0
        sleeptime = 0.1
        # while camera.motor.is_homed: doesn't work because it takes every action before and does it

        '''
        self.action = False in maze_camera
        
        '''

        while True:
            if not camera.row_enter:
                self.cursor.pos_hint = KeyboardObjectList[index].pos_hint
                try:
                    KeyboardObjectList[index].color = "white"
                    KeyboardObjectList[index + 1].color = "lightblue"
                    KeyboardObjectList[index - 1].color = "lightblue"
                except IndexError:
                    pass
                if camera.key_right and index < 29:
                    index += 1
                    camera.key_right = False
                if camera.key_left and index > 0:
                    index -= 1
                    camera.key_left = False
                if camera.delete:
                    self.Delete_Key_Update()
                    camera.delete = False
                if camera.row_top:
                    if index > 9:
                        index -= 1
                    self.bar.pos_hint = self.top_row_pos_hint
                    camera.row_middle = False
                    camera.row_bottom = False
                    sleep(sleeptime)
                if camera.row_middle:
                    if index < 10:
                        index += 1
                    if index > 19:
                        index -= 1
                    self.bar.pos_hint = self.middle_row_pos_hint
                    camera.row_top = False
                    camera.row_bottom = False
                    sleep(sleeptime)
                if camera.row_bottom:
                    if index < 20:
                        index += 1
                    self.bar.pos_hint = self.bottom_row_pos_hint
                    camera.row_top = False
                    camera.row_middle = False
                    sleep(sleeptime)
                if camera.clicked:
                    try:
                        for thing in KeyboardObjectList:
                            if self.cursor.collide_widget(thing):
                                thing.trigger_action(duration=0.1)
                                thing.color = (1, 1, 1, 0.89)
                                sleep(0.2)
                                thing.color = "lightblue"
                                camera.clicked = False
                    except Exception as e:
                        print(e, 'in click, not a button')
            elif camera.row_enter:
                self.Enter_Key_Update()
                break

            sleep(0.1)

    def set_keyboard_keys(self):
        KeyboardObjectList = [self.a1, self.b1, self.c1, self.d1, self.e1, self.f1, self.g1, self.h1, self.i1, self.j1,
                              self.k1, self.l1, self.m1, self.n1, self.o1, self.p1, self.q1, self.r1, self.s1,
                              self.space,
                              self.t1, self.u1, self.v1, self.w1, self.x1, self.y1, self.z1, self.star, self.dash,
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
        self.enterKey.color = "blue"
        self.enterKey.text = ""
        self.nickname.color = "lightblue"
        self.nickname.text = "Enter Your Name:"

        self.bar.pos_hint = self.top_row_pos_hint
        self.bar.size_hint = self.bar_size_hint

        # self.cursor.pos_hint = {"x": .0115, "y": .54}
        self.cursor.pos_hint = KeyboardObjectList[1].pos_hint
        self.cursor.size_hint = self.cursor_size_hint



    def Key_Update(self, button):
        if ":" in self.nickname.text or "!" in self.nickname.text:
            self.nickname.text = ""
        self.nickname.text += button.text

    def Delete_Key_Update(self):
        if len(self.nickname.text) > 0:
            self.nickname.text = self.nickname.text[:-1]

    def Enter_Key_Update(self):
        print('trying to press enter')

        if len(self.nickname.text) >= 1 and ":" not in self.nickname.text and "!" not in self.nickname.text:
            with open("leaderboard.txt", "a") as f:
                f.write(score + " ")
                f.write(self.nickname.text + "\n")
            self.nickname.text = "Congratulations!"
            Clock.schedule_once(self.transition)
        else:
            self.nickname.text = "Not A Name!"
        camera.row_enter = False

    def transition(self, dt):
        SCREEN_MANAGER.current = LEADERBOARD_SCREEN_NAME # undo when transfer

class LeaderboardScreen(Screen):
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
            score_board += str(count) + ". " + pairs[count][1] + ": " + pairs[count][0] + " seconds\n"
            count += 1

        self.leaderboard.text = score_board
        Clock.schedule_once(self.transition, 5)
        sleep(1)
        # self.leaderboard.text = ""
        # self.leaderboard_greeting.text = "Thank you\nfor playing!"


    def transition(self, dt):
        sleep(10)
        SCREEN_MANAGER.current = START_SCREEN_NAME


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
