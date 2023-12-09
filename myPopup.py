from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.graphics import Callback, Rectangle, Color
from myLayout import MyStackLayout, MyBoxLayout
from myButton import MyButtonBorder
from kivyFunctions import normal_color, border_color
from functions import rootFolder

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

class ModalWindow(MyBoxLayout):

    def __init__(self, dialog,  **kwargs):
        super().__init__( **kwargs)
        self.dialog = dialog
        self.orientation = 'vertical'
        self.clear_widgets()
        self.canvas.add(Callback(self.update_layout))
        self.dialog.auto_dismiss = False

    def update_layout(self, instr):
        self.draw_title()
        super().update_layout(instr)


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


class Dialog(ModalWindow):
    def __init__(self, dialog, text='', txtOk='OK', txtCancel='Cancel', icon='', **kwargs):
        super().__init__(dialog, **kwargs)

        textLayout = GridLayout()
        textLayout.cols = 3
        textLayout.padding = (16, 0, 16, 0)
        label = Label(text=text)
        self.size = label.size
        self.label = label
        self.icon = None
        if icon != '':
            separator = BoxLayout()
            separator.size_hint = (None, 1)
            separator.width = 32
            if icon == 'exclamation':
                icon = Image(source=rootFolder + 'images/icon_exclamation.png')
            icon.fit_mode = 'scale-down'
            icon.size_hint = (None, 1)
            icon.width = 48
            self.icon = icon
            textLayout.add_widget(icon)
            textLayout.add_widget(separator)
        textLayout.add_widget(label)
        self.add_widget(textLayout)

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

    def update_layout(self, instr):
        label = self.label
        if self.icon:
            self.dialog.width = label.texture_size[0] + self.icon.width + 64
        else:
            self.dialog.width = label.texture_size[0] + 64
        self.dialog.height = self.dialog.initialHeight + label.texture_size[1] + 64
        self.dialog.height += self.boxButtons.height
        super().update_layout(instr)

    def btnCancel_on_press(self, widget):
        self.dialog.dismiss()

class Progress(ModalWindow):

    def __init__(self,  dialog, max=100,  text='', **kwargs):
        super().__init__(dialog, **kwargs)
        self.padding = [16, 0, 16, 0]

        layout1 = AnchorLayout()
        layout1.anchor_x = 'left'
        layout1.anchor_y = 'bottom'
        label = Label(text=text)
        label.height = 32
        label.size_hint = (None, None)
        layout1.add_widget(label)

        layout2 = AnchorLayout()
        layout2.anchor_x = 'center'
        layout2.anchor_y = 'top'
        progress = ProgressBar(max=max)
        progress.size_hint = (1, None)
        layout2.add_widget(progress)

        self.add_widget(layout1)
        self.add_widget(layout2)
        self.dialog = dialog
        self.progress = progress
        self.label = label

    def update_layout(self, instr):
        self.label.width = self.label.texture_size[0]
        self.progress.size = self.label.size
        super().update_layout(instr)

    def update_progress(self, value, message):
        self.progress.value = value
        self.label.text = message
        print(message)