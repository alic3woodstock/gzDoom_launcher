from kivy.graphics import Callback, Color, Rectangle
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import CoreLabel
from myLayout import MyBoxLayout
from myButton import text_color, highlight_color, background_color, button_height


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
        menuItem.bind(on_press=lambda btn: self.select(menuItem))
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
        self.width = 0
        for btn in self.layout.children:
            if btn.texture_size[0] > self.width:
                self.width = btn.texture_size[0] + 16

class MenuItem(Button):
    def __init__(self, index, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.height = button_height
        self.canvas.add(Callback(self.update_button))
        self.hover = False

    def update_button(self, instr):
        padding = [self.width / 2 - self.texture_size[0] / 2, self.height / 2 - self.texture_size[1] / 2]
        label = CoreLabel(text=self.text, color=text_color,
                          font_size=self.font_size, font=self.font_name,
                          halign='center', valign='center', padding=padding)
        label.refresh()
        if self.state == 'normal':
            self.background_color = background_color
            self.color = text_color
            with self.canvas.after:
                if self.hover:
                    self.background_color = highlight_color
                    Color(rgba=highlight_color)
                else:
                    Color(rgba=background_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(rgba=text_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)
        else:
            self.background_color = text_color
            self.color = background_color
            with self.canvas.after:
                Color(rgba=highlight_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(rgba=text_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)

