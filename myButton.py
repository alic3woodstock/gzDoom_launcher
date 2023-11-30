from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

import kivyFunctions
from kivyFunctions import change_color


class MyButton(Button):
    def __init__(self, **kwargs):
        Clock.schedule_once(lambda *args: self.get_absolute_pos())
        super().__init__(**kwargs)
        change_color(self)
        Window.bind(mouse_pos=self.on_mouseover)
        Window.bind(on_cursor_leave=self.cursor_leave)

    def get_absolute_pos(self):
        self.absX = self.x
        self.absY = Window.height - self.top - (68 * 2)
        self.absTop = Window.height - self.y - 68
        self.absRight = self.right
        print(self.y)
        print(self.top)

    def on_mouseover(self, window, pos):
        if self.state == 'normal':
            if self.collide_abs_point(*pos):
                self.background_color = kivyFunctions.hover_color
            else:
                change_color(self)

    def cursor_leave(self, window):
        change_color(self)

    def collide_abs_point(self, x, y):
        return self.absX <= x <= self.right and self.absY <= y <= self.absTop


class MyToggleButton(ToggleButtonBehavior, MyButton):
    def __init__(self, **kwargs):
        Clock.schedule_once(lambda *args: self.get_absolute_pos())
        super().__init__(**kwargs)

    def on_state(self, widget, value):
        change_color(self)
        self.on_mouseover(None, (self.absX, self.absY))


