from kivy.graphics import Callback, Color, Rectangle
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import CoreLabel
from myLayout import MyBoxLayout
from kivyFunctions import button_height, border_color, normal_color, normal_highlight_color


class Menu(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.sync_height = False
        self.auto_width = False
        self.width = 256
        layout = MyBoxLayout()
        layout.size_hint = (1, None)
        layout.lineWidth = 1
        layout.orientation = 'vertical'
        self.layout = layout
        self.add_widget(layout)
        self.topButton = None

    def add_item(self, text):
        index = len(self.layout.children)
        menuItem = MenuItem(index=index, text=text)
        menuItem.bind(on_press=lambda btn: self.select(menuItem.index))
        self.layout.height = button_height * (index + 1)
        self.layout.add_widget(menuItem)

    def on_dismiss(self):
        if self.topButton:
            self.topButton.state = 'normal'
        super().on_dismiss()

    def open(self, widget):
        super().open(widget)
        self.topButton = self.attach_to
        self.topButton.state = 'down'

class MenuItem(Button):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.height = button_height
        self.canvas.add(Callback(self.update_button))

    def update_button(self, instr):
        padding = [self.width / 2 - self.texture_size[0] / 2, self.height / 2 - self.texture_size[1] / 2]
        label = CoreLabel(text=self.text, color=border_color,
                          font_size=self.font_size, font=self.font_name,
                          halign='center', valign='center', padding=padding)
        label.refresh()
        if self.state == 'normal':
            self.background_color = normal_color
            self.color = border_color
            with self.canvas.after:
                Color(rgba=normal_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(rgba=border_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)
        else:
            self.background_color = border_color
            self.color = normal_color
            with self.canvas.after:
                Color(rgba=normal_highlight_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(rgba=border_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)
