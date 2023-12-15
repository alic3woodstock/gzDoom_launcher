from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Callback, Color, Rectangle
from kivy.metrics import Metrics
from kivy.uix.relativelayout import RelativeLayout

from icon import Icon
from myButton import MyButtonBorder, MyButton, text_color, background_color
from myLayout import MyBoxLayout



class VertScrollBar(MyBoxLayout):

    def __init__(self, scroll, container, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, 1)
        self.width = 20
        self.scroll = scroll
        self.lineWidth = 1

        topButton = MyButtonBorder(icon=Icon('uparrow'))
        topButton.size_hint = (1, None)
        topButton.height = self.width
        topButton.bind(on_press=self.move_scroll)
        self.topButton = topButton
        self.add_widget(topButton)

        trail = RelativeLayout()
        self.add_widget(trail)

        trailButton = MyButtonBorder()
        trailButton.background_color = text_color
        trailButton.highlight_color = text_color
        trailButton.size_hint = (1, None)
        trail.pos = (0, 0)
        trail.add_widget(trailButton)
        trailButton.pos_hint = {'y': 0}
        trailButton.center = trail.center
        trailButton.bind(on_touch_down=self.btn_on_touch_down)
        self.trail=trail
        self.trailButton = trailButton


        bottomButton = MyButtonBorder(icon=Icon('downarrow'))
        bottomButton.size_hint = (1, None)
        bottomButton.height = self.width
        bottomButton.bind(on_press=self.move_scroll)
        self.bottomButton = bottomButton
        self.add_widget(bottomButton)
        self.const = 0
        self.initPos = 0
        Window.bind(mouse_pos=self.mouse_pos)
        self.cb = Callback(self.scroll_update)
        self.canvas.add(self.cb)
        self.movup = False
        self.movdown = False

    def scroll_update(self, widget=None):
        height1 = (self.scroll.height / self.scroll.viewport_size[1] * self.trail.height)
        if height1 > self.width:
            self.trailButton.height = height1
        else:
            self.trailButton.height = self.width

        const = (self.trail.height - self.trailButton.height) / self.trail.height
        self.const = const

        if self.trailButton.state == 'normal' and self.parent:
            movment = self.scroll.scroll_y * const
            if movment < 0:
                movment = 0
            if movment > const:
                movment = const
            self.trailButton.pos_hint = {'y': movment}
            self.canvas.ask_update()

        self.on_state(self.topButton, self.topButton.state)
        self.on_state(self.bottomButton, self.bottomButton.state)

        if self.movup:
            Clock.schedule_once(partial(self.move_scroll, self.topButton, 0), 0.1)
        elif self.movdown:
            Clock.schedule_once(partial(self.move_scroll, self.bottomButton, 0), 0.1)
        else:
            Clock.unschedule(partial(self.move_scroll, self.topButton, 0))
            Clock.unschedule(partial(self.move_scroll, self.bottomButton, 0))

    def btn_on_touch_down(self, touch, event):
        pos = Window.mouse_pos
        y = pos[1] * Metrics.dpi / 96
        pos = touch.to_window(*touch.pos)
        self.initPos = y - pos[1]

    def mouse_pos(self, *args):
        if self.trailButton.state == 'down':
            pos = args[1]
            y = pos[1] * Metrics.dpi / 96
            pos = self.trail.to_window(*self.trail.pos)
            y = y - pos[1] - self.initPos
            mov_scroll = y / self.trail.height
            if mov_scroll < 0:
                mov_scroll = 0
            if mov_scroll > self.const:
                mov_scroll = self.const
            self.trailButton.pos_hint = {'y': mov_scroll}
            y = mov_scroll / self.const
            self.scroll.scroll_y = y
            self.canvas.ask_update()

    def move_scroll(self, widget, value=0, *args):
        qtd = self.scroll.convert_distance_to_scroll(0, self.scroll.scroll_distance)
        if widget == self.topButton:
            self.scroll.scroll_y = (self.scroll.scroll_y + qtd[1])
        else:
            self.scroll.scroll_y = (self.scroll.scroll_y - qtd[1])
        if self.scroll.scroll_y < 0:
            self.scroll.scroll_y = 0
        if self.scroll.scroll_y > 1:
            self.scroll.scroll_y = 1

    def on_state(self, widget, value):
        if widget.state == 'down':
            Clock.schedule_once(partial(self.change_movement, widget, 0), 0.5)
        else:
            Clock.unschedule(partial(self.change_movement, widget, 0))
            if widget == self.topButton:
                self.movup = False
            else:
                self.movdown = False

    def change_movement(self, widget, value, *args):
        self.movup = widget == self.topButton
        self.movdown = widget == self.bottomButton
