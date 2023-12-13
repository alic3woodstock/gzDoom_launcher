import math

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.graphics import Callback, Rectangle, Color, Line, Ellipse
from myLayout import MyStackLayout, MyBoxLayout
from myButton import MyButtonBorder, text_color, background_color, highlight_color

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

class Icon(Widget):

    def __init__(self, icon='information', **kwargs):
        super().__init__(**kwargs)
        self.icon = icon
        self.canvas.add(Callback(self.draw_icon))

    def draw_icon(self, instr):
        self.canvas.after.clear()
        pos_center = self.to_window(*self.center)
        pos = self.to_window(*self.pos)
        if self.width > self.height:
            size = self.height
            x = pos_center[0] - size / 2
            y = pos[1]
        else:
            size = self.width
            x = pos[0]
            y = pos_center[1] - size / 2

        with self.canvas.after:
            Color(rgba=text_color)
            if self.icon == 'exclamation':
                point_t1 = (x, y)
                point_t2 = (pos_center[0] - 0.1, y + size)
                point_t3 = (x + size, y)
                point1 = (pos_center[0], y + 8)
                point2 = (pos_center[0], y + 16)
                point3 = (pos_center[0], y + size - 16)
                Line(points=[point_t1, point_t2, point_t3], width=1.1, close=True)
                Line(points=[point1, point1], width=2)
                Line(points=[point2, point3], width=2)
            elif self.icon == 'pentagram':
                Color(rgba=[1, 0, 0, 1])
                cx1 = math.sin(2 * math.pi / 5)
                cx2 = math.sin(4 * math.pi / 5)
                cy1 = math.cos(2 * math.pi / 5)
                cy2 = math.cos(math.pi / 5)
                cx1 = cx1 * size / 2
                cx2 = cx2 * size / 2
                cy1 = cy1 * size / 2
                cy2 = cy2 * size / 2
                point1 = (pos_center[0], y)
                point4 = (pos_center[0] + cx1, pos_center[1] - cy1)
                point5 = (pos_center[0] - cx2, pos_center[1] + cy2)
                point2 = (pos_center[0] + cx2, pos_center[1] + cy2)
                point3 = (pos_center[0] - cx1, pos_center[1] - cy1)
                Line(points=[point1, point2, point3, point4, point5], width=1.1, close=True)
                Line(ellipse=(x, y, size, size), width=1.1)
            else:
                point1 = (pos_center[0], y + 12)
                point2 = (pos_center[0], y + size - 20)
                point3 = (pos_center[0], y + size - 12)
                Line(ellipse=(x, y, size, size), width=1.1)
                Line(points=[point1, point2], width=2)
                Line(points=[point3, point3], width=2)


        self.canvas.ask_update()

class ModalForm(ModalWindow):

    def __init__(self, dialog, txtOk = 'OK', txtCancel='Cancel', **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size

        self.topLayout = GridLayout(cols=2)
        self.topLayout.padding = 16
        self.add_widget(self.topLayout)
        self.CreateBoxButtons(txtOk, txtCancel)
