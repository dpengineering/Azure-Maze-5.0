from imports.kivy_imports import *


class KinectGUI(App):

    def build(self):
        layout = FloatLayout()
        def add_widget(widget):
            layout.add_widget(widget)
        timer = Label(text="timer", size_hint=(0.5, 1))
        add_widget(timer)
        return layout


if __name__ == '__main__':
    KinectGUI().run()
