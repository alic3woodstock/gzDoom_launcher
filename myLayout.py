from functools import partial

import screeninfo
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
        icon = Icon('pentagram')
        icon.buttonMargin = 10
        self.icon = MyButton(icon=icon)
        self.icon.size_hint = (None, None)
        self.add_widget(self.icon)
        self.canvas.add(Callback(self.update_layout))

    def update_layout(self, instr):
        self.icon.height = self.height - self.padding[0] * 2
        self.icon.width = self.height - self.padding[1] * 2


class SystemIcons(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.btnMove = MyButton()
        self.btnMove.size_hint = (1, 1)
        self.btnMove.highlight_color = self.btnMove.background_color

        icon = Icon('minimize')
        icon.buttonMargin = 13
        self.minButton = MyButton(icon=icon)
        self.minButton.size_hint = (None, None)
        self.minButton.bind(on_release=self.minimize_event)

        icon = Icon('restore')
        icon.buttonMargin = 13
        self.restoreIcon = icon
        icon = Icon('maximize')
        icon.buttonMargin = 13
        self.maxIcon = icon
        self.maxButton = MyButton(icon=icon)
        self.maxButton.size_hint = (None, None)
        self.maxButton.bind(on_release=self.maximize_event)

        icon = Icon('close')
        icon.buttonMargin = 13
        self.closeButton = MyButton(icon=icon)
        self.closeButton.size_hint = (None, None)
        self.closeButton.bind(on_release=self.close_event)

        self.add_widget(self.btnMove)
        self.add_widget(self.minButton)
        self.add_widget(self.maxButton)
        self.add_widget(self.closeButton)

        self.canvas.add(Callback(self.update_layout))
        self.old_size = Window.system_size
        self.old_pos = (Window.left, Window.top)
        self.maximized = False
        self.is_moving = False
        self.window_origin = (0, 0)
        self.monitor = screeninfo.get_monitors()

    def update_layout(self, instr):
        self.maxButton.size = (self.height, self.height)
        self.minButton.size = (self.height, self.height)
        self.closeButton.size = (self.height, self.height)
        # self.width = self.height * 3
        if not self.maximized:
            self.old_pos = (Window.left, Window.top)
        self.canvas.ask_update()
        Window.bind(on_mouse_move=self.mouse_move)
        Window.bind(on_mouse_down=self.mouse_down)
        Window.bind(on_mouse_up=self.mouse_up)
        self.monitor = screeninfo.get_monitors()

    def close_event(self, widget):
        Window.close()

    def maximize_event(self, widget):
        if self.maximized:
            self.maximized = False
            x = self.old_size[0]
            y = self.old_size[1]
            Window.size = (x, y)
            Window.left = self.old_pos[0]
            Window.top = self.old_pos[1]
            Window.always_on_top = False
            widget.icon = self.maxIcon
        else:
            self.maximized = True
            monitor = self.monitor[0]
            if Window.left > monitor.width or Window.left < monitor.x:
                monitor = self.monitor[1]
            x = monitor.width / Metrics.dpi * 96
            y = monitor.height / Metrics.dpi * 96
            Window.system_size = (x, y)
            Window.top = monitor.y
            Window.left = monitor.x
            Window.always_on_top = True
            widget.icon = self.restoreIcon
        widget.canvas.ask_update()

    def minimize_event(self, widget):
        Window.minimize()

    def mouse_down(self, widget, x, y, button, modifiers):
        self.window_origin = (x, y)
        x = x * Metrics.dpi / 96
        y = Window.height - y * Metrics.dpi / 96
        if self.btnMove.collide_point(*self.btnMove.to_widget(x, y)):
            self.is_moving = True

    def mouse_move(self, widget, x, y, modifiers):
        if self.is_moving and (not self.maximized):
            Clock.schedule_once(partial(self.move_schedule, x, y), 0)

    def mouse_up(self, widget, x, y, button, modifiers):
        if self.is_moving:
            Window.system_size = (799, 599)
            Clock.schedule_once(self.restore_size_schedule, 0)
        self.is_moving = False

    def move_schedule(self, x, y, *args):
        x = self.window_origin[0] - x
        y = self.window_origin[1] - y
        Window.left = Window.left - x
        Window.top = Window.top - y

    def restore_size_schedule(self, *args):
        Window.system_size = self.old_size
        Window.canvas.ask_update()

