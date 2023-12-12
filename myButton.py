from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Callback
from kivyFunctions import change_color, border_color


class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        change_color(self)

    def on_state(self, instance, value):
        change_color(self)

class MyToggleButton(ToggleButtonBehavior, MyButton):
    pass


class MyButtonBorder(MyButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.canvas.add(Callback(self.update_button))

    def draw_border(self):
        self.canvas.after.clear()
        if self.width > 2:
            with self.canvas.after:
                Color(border_color)
                point1 = self.pos
                point2 = (self.x + self.width, self.y)
                point3 = (self.x + self.width, self.y + self.height)
                point4 = (self.x, self.y + self.height)
                Line(points=[point1, point2, point3, point4, point1], width=1)

    def update_button(self, instr):
        self.draw_border()
        change_color(self)
        self.canvas.ask_update()


class DropdownItem(ToggleButtonBehavior, MyButtonBorder):

    def draw_border(self):
        super().draw_border()
        with self.canvas.after:
            Color(border_color)
            center = self.y + self.height // 2
            point1 = (self.x + self.width - 32, center + 4)
            point2 = (self.x + self.width - 24, center - 4)
            point3 = (self.x + self.width - 16, center + 4)
            Line(points=[point1, point2, point3], width=1.5)


class topMenuButton(MyToggleButton):
    def __init__(self, dropdown, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        if dropdown:
            dropdown.bind(on_dismiss=self.on_dropdown_dismiss)
        self.dropdown = dropdown
        self.canvas.add(Callback(self.update_button))
        self.isDropOpen = False

    def on_release(self, value=0):
        self.dropdown.open(self)
        self.isDropOpen = True
        topPanel = self.dropdown.parent
        for btn in topPanel.children:
            if not (btn == self):
                btn.state = 'normal'

    def on_dropdown_dismiss(self, widget):
        self.isDropOpen = False

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
