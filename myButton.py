from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

import kivyFunctions
from kivyFunctions import change_color


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kivyFunctions.change_color(self)

    def on_press(self):
        kivyFunctions.change_color(self)

    def on_release(self):
        change_color(self)

class MyToggleButton(ToggleButtonBehavior, MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_state(self, widget, value):
        change_color(self)

