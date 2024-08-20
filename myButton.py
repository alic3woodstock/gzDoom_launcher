from kivy.graphics import Color, Line, Callback, Rectangle
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import CoreLabel

from functions import text_color, highlight_color, background_color, button_height
from icon import Icon


class MyButton(Button):
    def __init__(self, icon=None, **kwargs):
        super().__init__(**kwargs)
        self.hover = False
        self.canvas.add(Callback(self.update_button))
        self.text_color = text_color
        self.highlight_color = highlight_color
        self.hover_color = highlight_color
        self.background_color = background_color
        self.icon = icon

    def draw_button(self):
        padding = [self.width / 2 - self.texture_size[0] / 2, self.height / 2 - self.texture_size[1] / 2]
        label = CoreLabel(text=self.text, color=self.text_color,
                          font_size=self.font_size, font=self.font_name,
                          halign='center', valign='center', padding=padding)
        label.refresh()
        if self.state == 'normal':
            with self.canvas.after:
                if self.hover:
                    Color(rgba=self.hover_color)
                else:
                    Color(rgba=self.background_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(rgba=self.text_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)
        else:
            with self.canvas.after:
                Color(rgba=self.highlight_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                if self.text_color == self.highlight_color:
                    Color(rgba=self.background_color)
                else:
                    Color(rgba=self.text_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)

        if self.icon:
            self.icon.size = (self.width - self.icon.buttonMargin * 2, self.height - self.icon.buttonMargin * 2)
            self.icon.center = self.center
            for i in self.icon.get_instr():
                self.canvas.after.add(i)

    def update_button(self, instr):
        self.canvas.after.clear()
        self.draw_button()
        self.canvas.ask_update()


class MyToggleButton(ToggleButtonBehavior, MyButton):
    pass


class MyButtonBorder(MyButton):
    def __init__(self, icon=None, **kwargs):
        super().__init__(icon, **kwargs)
        self.size_hint = (1, None)
        self.border_color = text_color

    def draw_border(self):
        if self.width > 2:
            with self.canvas.after:
                Color(rgba=self.border_color)
                point1 = self.pos
                point2 = (self.x + self.width, self.y)
                point3 = (self.x + self.width, self.y + self.height)
                point4 = (self.x, self.y + self.height)
                Line(points=[point1, point2, point3, point4], width=1, close=True)

    def update_button(self, instr):
        self.canvas.after.clear()
        self.draw_button()
        self.draw_border()
        self.canvas.ask_update()


class DropdownMainButton(ToggleButtonBehavior, MyButtonBorder):

    def draw_border(self):
        super().draw_border()
        with self.canvas.after:
            Color(text_color)
            center = self.y + self.height // 2
            point1 = (self.x + self.width - 32, center + 4)
            point2 = (self.x + self.width - 24, center - 4)
            point3 = (self.x + self.width - 16, center + 4)
            Line(points=[point1, point2, point3], width=1.5)


class TopMenuButton(MyToggleButton):
    def __init__(self, dropdown, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        if dropdown:
            dropdown.bind(on_dismiss=self.on_dropdown_dismiss)
        self.dropdown = dropdown
        self.highlight_color = self.hover_color
        self.canvas.add(Callback(self.update_button))
        self.isDropOpen = False

    def on_release(self, value=0):
        self.dropdown.open(self)
        self.isDropOpen = True
        topPanel = self.dropdown.parent
        for btn in topPanel.children:
            if not (btn == self):
                btn.state = 'normal'

    def on_dropdown_dismiss(self, _widget):
        self.isDropOpen = False

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
        super().update_button(instr)


class MyCheckBox(MyToggleButton):

    def __init__(self, **kwargs):
        super().__init__(icon=Icon('maximize'), **kwargs)
        self.highlight_color = self.background_color
        self.active = False

    def choose_icon(self):
        if self.state == 'down':
            self.icon = Icon('check', color=highlight_color, line_width=1)
        else:
            self.icon = Icon('maximize', line_width=1)
        self.active = self.state == 'down'
        self.icon.buttonMargin = 0

    def update_button(self, instr):
        self.canvas.after.clear()
        self.choose_icon()
        self.draw_button()
        self.canvas.ask_update()

class DropDownItem(MyButtonBorder):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.height = button_height
        if game:
            self.text = game.name

    def on_press(self):
        if self.parent and self.parent.parent:
            dropDown = self.parent.parent
            dropDown.select(self.game)
