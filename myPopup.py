from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Callback, Rectangle, Color, Line

from icon import Icon
from myLayout import MyStackLayout, MyBoxLayout
from myButton import MyButtonBorder, text_color, background_color


class MyPopup(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.size_hint = (None, None)
        self.background_color = background_color
        self.separator_color = text_color
        self.initialHeight = self.height
        self.title_color = background_color
        self.separator_height = 2
        self.is_open = False

    def on_open(self):
        super().on_open()
        self.is_open = True

    def on_dismiss(self):
        super().on_dismiss()
        self.is_open = False

class ModalWindow(MyBoxLayout):

    def __init__(self, dialog, **kwargs):
        super().__init__( **kwargs)
        self.dialog = dialog
        self.orientation = 'vertical'
        self.clear_widgets()
        self.canvas.add(Callback(self.update_layout))
        self.dialog.auto_dismiss = False
        self.buttons = []

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
            title.background_color = text_color
            title.canvas.after.clear()
            pos_y = title.y + title.height / 2 - title.texture_size[1] / 2 - self.lineWidth * 2
            self.dialog.canvas.after.clear()
            with self.dialog.canvas.after:
                Color(rgba=text_color)
                Rectangle(pos=(self.x - self.lineWidth, title.y - self.lineWidth * 2),
                          size=(self.width + self.lineWidth * 2, title.height))
                Color(rgba=background_color)
                Rectangle(pos=(title.x + 8, pos_y), size=title.texture_size, texture=title.texture)

    def CreateBoxButtons(self, txtOk, txtCancel):
        boxButtons = MyStackLayout()
        boxButtons.size_hint = (1, None)
        boxButtons.height = 64
        boxButtons.borders = ['top']
        boxButtons.orientation = 'rl-tb'
        boxButtons.padding = (8, 10, 8, 8)
        self.add_widget(boxButtons)
        self.boxButtons = boxButtons

        if txtCancel.strip():
            btnCancel = MyButtonBorder()
            btnCancel.size_hint = (None, 1)
            btnCancel.text = txtCancel
            btnCancel.width = 128
            btnCancel.bind(on_press=self.btnCancel_on_press)
            boxButtons.add_widget(btnCancel)
            self.btnCancel = btnCancel

        if txtOk.strip():
            self.btnOk = self.AddButon(txtOk)

    def btnCancel_on_press(self, widget):
        self.dialog.dismiss()

    def AddButon(self, txtBtn=''):
        blankLabel = Label()
        blankLabel.size_hint = (None, 1)
        blankLabel.width = 8
        self.boxButtons.add_widget(blankLabel)

        btnOk = MyButtonBorder()
        btnOk.size_hint = (None, 1)
        btnOk.text = txtBtn
        btnOk.width = 128
        self.boxButtons.add_widget(btnOk)
        return btnOk


class Dialog(ModalWindow):
    def __init__(self, dialog, text='', txtOk='OK', txtCancel='Cancel', icon='', **kwargs):
        super().__init__(dialog, **kwargs)

        textLayout = BoxLayout()
        textLayout.padding = (16, 0, 16, 0)
        label = Label(text=text)
        self.size = label.size
        self.label = label
        self.icon = None

        separator = BoxLayout()
        separator.size_hint = (None, 1)
        separator.width = 16
        icon = Icon(icon) # Image(source=rootFolder + 'images/icon_information.png')
        icon.size_hint = (None, 1)
        icon.width = 48
        self.icon = icon

        textLayout.add_widget(icon)
        textLayout.add_widget(separator)
        textLayout.add_widget(label)
        self.add_widget(textLayout)
        self.CreateBoxButtons(txtOk, txtCancel)


    def update_layout(self, instr):
        label = self.label
        if self.icon:
            self.dialog.width = label.texture_size[0] + self.icon.width + 80
        else:
            self.dialog.width = label.texture_size[0] + 64
        self.dialog.height = self.dialog.initialHeight + label.texture_size[1] + 64
        self.dialog.height += self.boxButtons.height
        super().update_layout(instr)

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
        progress = Widget()
        progress.size_hint = (1, None)
        layout2.add_widget(progress)

        self.add_widget(layout1)
        self.add_widget(layout2)
        self.dialog = dialog
        self.progress = progress
        self.max = max
        self.value = 0
        self.label = label

    def update_layout(self, instr):
        self.label.width = self.label.texture_size[0]
        self.progress.height = self.label.height
        self.draw_bar()
        super().update_layout(instr)

    def update_progress(self, value, message):
        self.value = value
        self.label.text = message
        self.draw_bar()

    def draw_bar(self):
        self.progress.canvas.after.clear()
        with self.progress.canvas.after:
            Color(rgba=text_color)

            pos = self.progress.to_window(self.progress.x, self.progress.center_y - 6)
            width = self.progress.width * self.value / self.max
            Rectangle(pos=pos, size=(width, 12))

            pos = self.progress.to_window(self.progress.x, self.progress.center_y)
            point1 = (pos[0], pos[1] + 6)
            point2 = (pos[0] + self.progress.width, pos[1] + 6)
            point3 = (pos[0] + self.progress.width, pos[1] - 6)
            point4 = (pos[0], pos[1] - 6)
            Line(points=[point1, point2, point3, point4, point1], width=1)


class ModalForm(ModalWindow):

    def __init__(self, dialog, txtOk = 'OK', txtCancel='Cancel', **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size

        self.topLayout = GridLayout(cols=2)
        self.topLayout.padding = 16
        self.add_widget(self.topLayout)
        self.CreateBoxButtons(txtOk, txtCancel)
