from kivy.uix.popup import Popup
from kivy.uix.label import Label, CoreLabel
from kivy.graphics import Callback, Rectangle, Color
from myLayout import MyStackLayout, MyBoxLayout
from myButton import MyButtonBorder
from kivyFunctions import normal_color, border_color

class MyPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.size_hint = (None, None)
        self.background_color = normal_color
        self.separator_color = border_color
        self.initialHeight = self.height
        self.title_color = normal_color
        self.separator_height = 2

class Dialog(MyBoxLayout):
    def __init__(self, dialog, text='', txtOk='OK', txtCancel='Cancel', **kwargs):
        super().__init__(**kwargs)
        self.dialog = dialog
        self.orientation = 'vertical'
        self.clear_widgets()

        label = Label(text=text)
        self.size = label.size
        self.add_widget(label)
        self.label = label

        boxButtons = MyStackLayout()
        boxButtons.size_hint = (1, None)
        boxButtons.height = 64
        boxButtons.borders = ['top']
        boxButtons.orientation = 'rl-tb'
        boxButtons.padding = (8, 10, 8, 8)
        self.add_widget(boxButtons)
        self.boxButtons = boxButtons

        btnCancel = MyButtonBorder()
        btnCancel.size_hint = (None, 1)
        btnCancel.text = txtCancel
        btnCancel.width = 128
        btnCancel.bind(on_press=self.btnCancel_on_press)
        boxButtons.add_widget(btnCancel)
        self.btnCancel = btnCancel

        blankLabel = Label()
        blankLabel.size_hint = (None, 1)
        blankLabel.width = 8
        boxButtons.add_widget(blankLabel)

        btnOk = MyButtonBorder()
        btnOk.size_hint = (None, 1)
        btnOk.text = txtOk
        btnOk.width = 128
        boxButtons.add_widget(btnOk)
        self.btnOk = btnOk

        self.canvas.add(Callback(self.update_layout))
        self.dialog.auto_dismiss = False

    def update_layout(self, instr):
        label = self.label
        self.dialog.width = label.texture_size[0] + 64
        self.dialog.height = self.dialog.initialHeight + label.texture_size[1] + 64
        self.dialog.height += self.boxButtons.height
        self.draw_title()
        super().update_layout(instr)

    def btnCancel_on_press(self, widget):
        self.dialog.dismiss()

    def draw_title(self):
        title = None
        for t in self.dialog.children[0].children:
            if isinstance(t, Label):
                title = t

        # self.height / 2 - self.texture_size[1] / 2

        if title:
            title.background_color = border_color
            title.canvas.after.clear()
            pos_y = title.y + title.height / 2 - title.texture_size[1] / 2 - self.lineWidth * 2
            self.dialog.canvas.after.clear()
            with self.dialog.canvas.after:
                Color(rgba=border_color)
                Rectangle(pos=(self.x - self.lineWidth, title.y - self.lineWidth * 2),
                          size=(self.width + self.lineWidth * 2, title.height))
                Color(rgba=normal_color)
                Rectangle(pos=(title.x + 8, pos_y), size=title.texture_size, texture=title.texture)


