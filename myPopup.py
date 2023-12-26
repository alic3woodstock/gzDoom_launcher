from kivy.clock import Clock
from kivy.graphics import Callback, Rectangle, Color, Line
from kivy.properties import AliasProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserProgress
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

import functions
from functions import text_color, background_color, button_height
from icon import Icon
from myButton import MyButtonBorder, MyButton
from myLayout import MyStackLayout, MyBoxLayout


class MyPopup(ModalView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = background_color
        self.size_hint = (None, None)

        self.topLayout = BoxLayout()
        self.topLayout.orientation = 'vertical'
        self.topLayout.padding = 0

        self.titleWidget = Label()
        icon = Icon('close', button_margin=10, color=background_color)
        self.closeButton = MyButton(icon=icon)
        self.closeButton.background_color = text_color
        self.closeButton.text_color = background_color
        self.closeButton.size_hint = (None, 1)
        self.closeButton.bind(on_release=(lambda dismiss: self.dismiss()))

        self.boxTitle = BoxLayout()
        self.boxTitle.padding = 0
        self.boxTitle.height = button_height
        self.closeButton.width = self.boxTitle.height

        self.boxTitle.add_widget(self.titleWidget)
        self.boxTitle.add_widget(self.closeButton)

        self.content = None
        self.boxContent = BoxLayout()

        self.title = ''
        self.is_open = False
        self.topLayout.add_widget(self.boxTitle)
        self.topLayout.add_widget(self.boxContent)
        self.add_widget(self.topLayout)
        self.canvas.add(Callback(self.update_popup))
        self.pre_open_size = 0

    def on_pre_open(self):
        self.topLayout.clear_widgets()
        self.opacity = 0

    def on_open(self):
        super().on_open()
        if self.titleWidget:
            self.titleWidget.text = self.title
        if self.content:
            self.boxContent.add_widget(self.content)
        self.is_open = True
        self.topLayout.add_widget(self.boxTitle)
        self.topLayout.add_widget(self.boxContent)

    def on_dismiss(self):
        super().on_dismiss()
        self.boxContent.clear_widgets()
        self.is_open = False

    def update_popup(self, instr):
        if len(self.boxContent.children) > 0 and self.boxContent.children[0] != self.content:
            self.boxContent.clear_widgets()
            self.boxContent.add_widget(self.content)
        self.closeButton.width = self.boxTitle.height
        if self.is_open and self.opacity < 1:
            Clock.schedule_once(lambda rp: self.redraw_popup(), 0.1)

    def redraw_popup(self):
        self.opacity += 0.5
        self.canvas.ask_update()


class ModalWindow(MyBoxLayout):

    def __init__(self, dialog, **kwargs):
        super().__init__(**kwargs)
        self.btnOk = None
        self.btnCancel = None
        self.boxButtons = None
        self.dialog = dialog
        self.orientation = 'vertical'
        self.clear_widgets()
        self.canvas.add(Callback(self.update_layout))
        if self.dialog:
            self.dialog.auto_dismiss = False
        self.buttons = []
        self.borders = ['left', 'bottom', 'right']

    def update_layout(self, instr):
        self.draw_title()
        super().update_layout(instr)

    def draw_title(self):
        if self.dialog:
            title = self.dialog.titleWidget
            if title:
                self.dialog.boxTitle.size_hint = (None, None)
                self.dialog.boxTitle.x = self.x - self.lineWidth
                self.dialog.boxTitle.width = self.width + self.lineWidth * 2
                self.dialog.boxTitle.height = button_height - self.lineWidth * 2
                functions.background_color = text_color
                title.canvas.after.clear()
                pos_y = title.y + title.height / 2 - title.texture_size[1] / 2
                self.dialog.canvas.after.clear()
                with self.dialog.canvas.after:
                    Color(rgba=text_color)
                    Rectangle(pos=title.pos,
                              size=(title.width, title.height + 1))
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
            btnCancel.bind(on_release=self.btnCancel_on_press)
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
        icon = Icon(icon)  # Image(source=rootFolder + 'images/icon_information.png')
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
        self.dialog.height = self.dialog.boxTitle.height + label.texture_size[1] + 64
        self.dialog.height += self.boxButtons.height
        super().update_layout(instr)


class Progress(ModalWindow):

    def __init__(self, dialog=None, max_value=100, text='', **kwargs):
        super().__init__(dialog, **kwargs)
        self.padding = [16, 0, 16, 0]

        layout1 = StackLayout()
        layout1.orientation = 'lr-bt'
        label = Label(text=text)
        label.height = 32
        label.size_hint = (None, None)
        layout1.add_widget(label)

        layout2 = StackLayout()
        progress = Widget()
        progress.size_hint = (1, None)
        layout2.add_widget(progress)

        self.add_widget(layout1)
        self.add_widget(layout2)
        self.dialog = dialog
        self.progress = progress
        self._value = 0
        self.label = label
        self.max = max_value

    max = NumericProperty(default=0)

    def _get_value(self):
        self.canvas.ask_update()
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'), cache=True)

    def update_layout(self, instr):
        self.label.width = self.label.texture_size[0]
        self.progress.height = self.label.height
        self.draw_bar()
        super().update_layout(instr)

    def update_progress(self, value, message):
        self.label.text = message
        self.value = value
        self.canvas.ask_update()

    def draw_bar(self):
        self.progress.canvas.after.clear()
        with self.progress.canvas.after:
            Color(rgba=text_color)

            pos = self.progress.to_window(self.progress.x, self.progress.center_y - 6)
            width = self.progress.width * self._value / self.max
            Rectangle(pos=pos, size=(width, 12))

            pos = self.progress.to_window(self.progress.x, self.progress.center_y)
            point1 = (pos[0], pos[1] + 6)
            point2 = (pos[0] + self.progress.width, pos[1] + 6)
            point3 = (pos[0] + self.progress.width, pos[1] - 6)
            point4 = (pos[0], pos[1] - 6)
            Line(points=[point1, point2, point3, point4, point1], width=1)


class FileProgress(FileChooserProgress):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()
        self.progress = Progress(max_value=self.total)
        self.progress.pos = (0, 0)
        self.progress.size = self.size
        self.add_widget(self.progress)
        self.canvas.add(Callback(self.update_layout))

    def update_layout(self, instr):
        self.progress.max = self.total
        self.progress.update_progress(self.index, str(self.index) + ' / ' + str(self.total))
