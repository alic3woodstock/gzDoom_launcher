from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Callback
from kivy.metrics import Metrics
from kivy.uix.relativelayout import RelativeLayout

from functions import text_color
from icon import Icon
from myButton import MyButtonBorder
from myLayout import MyBoxLayout


class VertScrollBar(MyBoxLayout):

    def __init__(self, scroll, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, 1)
        self.width = 20
        self.scroll = scroll
        self.scroll.bar_width = 0
        self.lineWidth = 1

        top_button = MyButtonBorder(icon=Icon('uparrow'))
        top_button.size_hint = (1, None)
        top_button.height = self.width
        top_button.bind(on_press=self.btn_move_scroll)
        self.topButton = top_button
        self.add_widget(top_button)

        trail = RelativeLayout()
        self.add_widget(trail)

        trail_button = MyButtonBorder()
        trail_button.background_color = text_color
        trail_button.highlight_color = text_color
        trail_button.size_hint = (1, None)
        trail.pos = (0, 0)
        trail.add_widget(trail_button)
        trail_button.pos_hint = {'y': 0}
        trail_button.center = trail.center
        self.trail = trail
        self.trailButton = trail_button

        bottom_button = MyButtonBorder(icon=Icon('downarrow'))
        bottom_button.size_hint = (1, None)
        bottom_button.height = self.width
        bottom_button.bind(on_press=self.btn_move_scroll)
        self.bottomButton = bottom_button
        self.add_widget(bottom_button)
        self.const = 0
        self.initPos = 0
        self.cb = Callback(self.scroll_update)
        self.canvas.add(self.cb)
        self.movup = False
        self.movdown = False
        self.movup2 = False
        self.movdown2 = False
        self.trailButton_pressed = False
        self.trail_pressed = False

        Window.bind(on_mouse_move=self.mouse_move)
        Window.bind(on_mouse_down=self.mouse_down)
        Window.bind(on_mouse_up=self.mouse_up)

    def scroll_update(self, _instr):
        if self.height > 0:
            height1 = (self.scroll.height / self.scroll.viewport_size[1] * self.trail.height)
            if height1 > self.width:
                self.trailButton.height = height1
            else:
                self.trailButton.height = self.width

            const = (self.trail.height - self.trailButton.height) / self.trail.height
            self.const = const

            if not self.trailButton_pressed and self.parent:
                movment = self.scroll.scroll_y * const
                if movment < 0:
                    movment = 0
                if movment > const:
                    movment = const
                self.trailButton.pos_hint = {'y': movment}
                self.canvas.ask_update()

            self.on_state(self.topButton, self.topButton.state)
            self.on_state(self.bottomButton, self.bottomButton.state)

            if self.movup or (self.movup2 and (self.scroll.scroll_y < self.trailpos_to_scroll())):
                Clock.schedule_once(partial(self.move_scroll, 'up', 0), 0.025)
            elif self.movdown or (self.movdown2 and (self.scroll.scroll_y > self.trailpos_to_scroll())):
                Clock.schedule_once(partial(self.move_scroll, 'down', 0), 0.025)
            else:
                Clock.unschedule(partial(self.move_scroll, 'up'))
                Clock.unschedule(partial(self.move_scroll, 'down'))

        # if self.trail.state == 'down':
        #     Clock.schedule_interval(self.trail_state_down, 0.1)
        # else:
        #     Clock.unschedule(self.trail_state_down)

    def mouse_down(self, _widget, x, y, button, _modifiers):
        x = x * Metrics.dpi / 96
        y = Window.height - y * Metrics.dpi / 96

        if button == 'left':
            if self.trailButton.collide_point(*self.trailButton.to_widget(x, y)):
                pos = self.trailButton.to_window(*self.trailButton.pos)
                self.initPos = y - pos[1]
                self.trailButton_pressed = True
            elif self.collide_point(*self.to_widget(x, y)):
                pos = self.trail.to_window(*self.trail.pos)
                y = y - pos[1]
                if (y >= 0) and y <= self.trail.height:
                    y = y / self.trail.height
                    if y < self.scroll.scroll_y:
                        self.movdown2 = True
                    elif y > self.scroll.scroll_y:
                        self.movup2 = True
                    else:
                        self.movup2 = False
                        self.movdown2 = False
                self.canvas.ask_update()

        if self.collide_point(*self.to_widget(x, y)):
            if button == 'scrolldown':
                self.move_scroll('up')
            if button == 'scrollup':
                self.move_scroll('down')

    def mouse_up(self, widget, _x, _y, _button, _modifiers):
        self.trailButton_pressed = False
        self.trail_pressed = False
        self.movup2 = False
        self.movdown2 = False
        Clock.unschedule(partial(self.change_movement, widget, 0))

    def mouse_move(self, _widget, _x, y, _modifiers):
        y = Window.height - y * Metrics.dpi / 96
        if self.trailButton_pressed:
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
        if self.movup2 or self.movdown2:
            self.canvas.ask_update()

    def btn_move_scroll(self, widget, _value, *_args):
        if widget == self.topButton:
            self.move_scroll()
        else:
            self.move_scroll('down')

    def move_scroll(self, direction='up', _value=0, *_args):
        qtd = self.scroll.convert_distance_to_scroll(0, self.scroll.scroll_distance)
        if direction == 'up':
            self.scroll.scroll_y = (self.scroll.scroll_y + qtd[1])
        else:
            self.scroll.scroll_y = (self.scroll.scroll_y - qtd[1])
        if self.scroll.scroll_y < 0:
            self.scroll.scroll_y = 0
        if self.scroll.scroll_y > 1:
            self.scroll.scroll_y = 1

    def on_state(self, widget, _value):
        if widget.state == 'down':
            Clock.schedule_once(partial(self.change_movement, widget, 0), 0.5)
        else:
            Clock.unschedule(partial(self.change_movement, widget, 0))
            if widget == self.topButton:
                self.movup = False
            else:
                self.movdown = False

    def change_movement(self, widget, _value, *_args):
        self.movup = widget == self.topButton
        self.movdown = widget == self.bottomButton

    def trailpos_to_scroll(self):
        pos = Window.mouse_pos
        y = pos[1] * Metrics.dpi / 96
        pos = self.trail.to_window(*self.trail.pos)
        y = y - pos[1]
        return y / self.trail.height
