from final.imports.imports import *
# timer here should be pretty simple. I haven't really used this class I made, but the code is clean so you can use it ig, but it's not needed for this project.

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


if __name__ == '__main__':
    timer = Timer()
    timer.start_timer()
    while True:
        print(timer.return_time())
        sleep(1)
