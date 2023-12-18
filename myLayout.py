from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.layout import Layout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Callback
from getBorders import GetBorders
from myButton import text_color


class MyLayout(Layout):
    borders = ['top', 'left', 'bottom', 'right']
    lineWidth = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
