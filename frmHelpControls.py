from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from functions import button_height
from genericForm import GenericForm
from myPopup import ModalWindow, MyPopup


class FrmHelpControls(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()

        self.genericForm = GenericForm()
        self.labels = []
        text = ['Left Arrow:', 'Previous Tab',
                'Right Arrow:', 'Next Tab',
                'Up Arrow:', 'Previous Game',
                'Down Arrow:', 'Next Game',
                'Space:', 'Change Mod',
                'Enter:', 'Run Game',
                'F11:', 'Fullscreen',
                'Esc:', 'Close Dialog / Exit']

        for i in range(0, len(text), 1):
            self.labels.append(Label(text=text[i], size_hint=(None, 1)))

        for i in range(0, len(text), 1):
            if i % 2 == 0:
                anchor = AnchorLayout(anchor_x='right')
                anchor.add_widget(self.labels[i])
            else:
                anchor = AnchorLayout(anchor_x='left')
                anchor.add_widget(self.labels[i])
            self.genericForm.topLayout.add_widget(anchor)

        self.add_widget(self.genericForm)

        self.create_box_buttons(
            '', 'Ok')
        self.canvas.add(Callback(self.update_form))
        self.dialog.height = (button_height * 2  # box buttons height + tithe height
                              + self.genericForm.get_height())

    def update_form(self, _instr):
        for label in self.labels:
            label.width = label.texture_size[0]
