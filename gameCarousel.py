from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Line, Callback, Rectangle
from kivy.uix.label import CoreLabel
from myLayout import MyStackLayout
from kivyFunctions import border_color, normal_color, GetBorders

class GameCarousel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        topPanel = MyStackLayout()
        topPanel.size_hint = (1, None)
        topPanel.height = 64
        topPanel.padding = (8, 18, 8, 0)
        carousel = Carousel()
        self.orientation = 'vertical'
        self.add_widget(topPanel)
        self.add_widget(carousel)
        self.carousel = carousel
        self.topPanel = topPanel

    def AddTab(self, name):
        btnTab1 = CarouselButton()
        btnTab1.text = name
        btnTab1.width = 200
        self.topPanel.add_widget(btnTab1)

class CarouselButton(ToggleButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.canvas.add(Callback(self.update_button))

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
        self.canvas.after.clear()
        self.change_color()
        self.canvas.ask_update()

    def change_color(self):
        padding = [8, self.height / 2 - self.texture_size[1] / 2]
        label = CoreLabel(text=self.text, color=normal_color,
                          font_size=self.font_size, font=self.font_name,
                          halign='center', valign='center', padding=padding)
        label.refresh()
        if self.state == 'normal':
            self.background_color = normal_color
            self.color = border_color
            borders = GetBorders(self)
            with self.canvas.after:
                Color(border_color)
                Line(points=[borders.top_left, borders.bottom_left, borders.bottom_right, borders.top_right],
                     width=1)
        else:
            with self.canvas.after:
                Color(border_color)
                Rectangle(pos=self.pos, size=self.size)
                Color(normal_color)
                text = label.texture
                print(self.texture_size)
                Rectangle(pos=self.pos, size=self.size, texture=text)


