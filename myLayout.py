import tkinter

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Callback
from getBorders import GetBorders
from icon import Icon
from myButton import text_color, MyButton


class MyLayout(Layout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.borders = ['top', 'left', 'bottom', 'right']
        self.lineWidth = 2
        self.canvas.add(Callback(self.update_layout))

    def draw_border(self):
        self.canvas.after.clear()
        borderPos = GetBorders(self)
        if self.width > 2:
            for b in self.borders:
                with self.canvas.after:
                    Color(text_color)
                    if b == 'left':
                        points = [borderPos.top_left, borderPos.bottom_left]
                    elif b == 'right':
                        points = [borderPos.top_right, borderPos.bottom_right]
                    elif b == 'bottom':
                        points = [borderPos.top_left, borderPos.top_right]
                    else:
                        points = [borderPos.bottom_left, borderPos.bottom_right]
                    Line(points=points, width=self.lineWidth)

    def update_layout(self, instr):
        self.draw_border()
        self.canvas.ask_update()


class MyStackLayout(MyLayout, StackLayout):
    pass


class MyBoxLayout(MyLayout, BoxLayout):
    pass

class RelativeLayoutButton(Button, RelativeLayout):
    pass

class TitleIcon(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = [4, 4, 4, 4]
        self.icon = MyButton(icon=Icon('pentagram'))
        self.icon.size_hint = (None, None)
        self.add_widget(self.icon)
        self.canvas.add(Callback(self.update_layout))

    def update_layout(self, instr):
        self.icon.height = self.height - self.padding[0] * 2
        self.icon.width = self.height - self.padding[1] * 2

    def in_drag_area(self, x, y):
        print('passou aqui')
        return self.collide_point(*self.to_window(x, y))

class SystemIcons(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = [4, 4, 4, 4]
        self.minButton = MyButton(text='-')
        self.minButton.size_hint = (None, None)
        self.maxButton = MyButton(text='+')
        self.maxButton.size_hint = (None, None)
        self.maxButton.bind(on_press=self.maximize_event)
        self.closeButton = MyButton(text='x')
        self.closeButton.size_hint = (None, None)
        self.closeButton.bind(on_press=self.close_event)
        self.add_widget(self.minButton)
        self.add_widget(self.maxButton)
        self.add_widget(self.closeButton)
        self.canvas.add(Callback(self.update_layout))
        self.old_size = Window.size

    def update_layout(self, instr):
        self.maxButton.size = (self.height, self.height)
        self.minButton.size = (self.height, self.height)
        self.closeButton.size = (self.height, self.height)
        self.width = self.height * 3

    def close_event(self, widget):
        Clock.schedule_once(exit, 0)

    def maximize_event(self, widget):
        Window.top = 0
        Window.left = 0
        app = tkinter.Tk()
        width = app.winfo_screenwidth()
        height = app.winfo_screenheight()
        x = width / Metrics.dpi * 96
        y = height / Metrics.dpi * 96
        Window.size = (x, y)
