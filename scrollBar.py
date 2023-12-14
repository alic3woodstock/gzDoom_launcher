from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Callback, Color, Rectangle
from kivy.metrics import Metrics
from kivy.uix.relativelayout import RelativeLayout

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

        topButton = MyButtonBorder()
        topButton.size_hint = (1, None)
        topButton.text = 'A' # replace with up arrow image
        topButton.height = self.width
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


        bottomButton = MyButtonBorder()
        bottomButton.size_hint = (1, None)
        bottomButton.text = 'V' # replace with down arrow image
        bottomButton.height = self.width
        self.bottomButton = bottomButton
        self.add_widget(bottomButton)
        self.const = 0
        self.pressed = False
        self.initPos = 0
        # Window.bind(on_touch_down=self.mouse_down)
        self.cb = Callback(self.scroll_update)
        self.canvas.add(self.cb)

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

    def btn_on_touch_down(self, touch, event):
        pos = Window.mouse_pos
        y = pos[1] * Metrics.dpi / 96
        pos = touch.to_window(*touch.pos)
        self.initPos = y - pos[1]

        Window.bind(mouse_pos=self.mouse_pos)

    def mouse_pos(self, *args):
        if self.trailButton.state == 'down':
            pos = args[1]
            y = pos[1] * Metrics.dpi / 96
            pos = self.trail.to_window(*self.trail.pos)
            y = y - pos[1] - self.initPos
            movment = y / self.trail.height
            if movment < 0:
                movment = 0
            if movment > self.const:
                movment = self.const
            self.trailButton.pos_hint = {'y': movment}
            y = movment / self.const
            self.scroll.scroll_y = y
            self.canvas.ask_update()
