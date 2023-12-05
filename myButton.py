from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Callback

import kivyFunctions
from kivyFunctions import change_color


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kivyFunctions.change_color(self)

    def on_state(self, instance, value):
        change_color(self)

class MyToggleButton(ToggleButtonBehavior, MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_state(self, widget, value):
        change_color(self)


class MyButtonBorder(MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.canvas.add(Callback(self.update_button))

    def draw_border(self, value=0):
        self.canvas.after.clear()
        if self.width > 2:
            with self.canvas.after:
                Color(kivyFunctions.border_color)
                point1 = self.pos
                point2 = (self.x + self.width, self.y)
                point3 = (self.x + self.width, self.y + self.height)
                point4 = (self.x, self.y + self.height)
                Line(points=[point1, point2, point3, point4, point1], width=1)

    def update_button(self, instr):
        self.draw_border()
        change_color(self)
        self.canvas.ask_update()


