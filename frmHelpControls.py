from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from genericForm import GenericForm
from myPopup import ModalWindow, MyPopup


class FrmHelpControls(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()

        self.genericForm = GenericForm()
        self.labels = []
        text = [_('Left Arrow:'), _('Previous Tab'),
                _('Right Arrow:'), _('Next Tab'),
                _('Up Arrow:'), _('Previous Game'),
                _('Down Arrow:'), _('Next Game'),
                _('Space:'), _('Change Mod'),
                _('Enter:'), _('Run Game'),
                'F11:', _('Fullscreen'),
                'Esc:', _('Close Dialog / Exit')]

        for i in range(0, len(text), 1):
            self.labels.append(Label(text=text[i], size_hint=(None, 1)))

        for i in range(0, len(text), 1):
            if i % 2 == 0:
                anchor = AnchorLayout(anchor_x='right')
                anchor.add_widget(self.labels[i])
            else:
                anchor = AnchorLayout(anchor_x='left')
                anchor.add_widget(self.labels[i])
            anchor.size_hint = (1, None)
            anchor.height = self.genericForm.children_height
            self.genericForm.topLayout.add_widget(anchor)

        self.add_widget(self.genericForm)

        self.create_box_buttons(
            '', 'Ok')
        self.dialog.height = 100
        self.canvas.add(Callback(self.update_form))

    def update_form(self, _instr):
        for label in self.labels:
            label.width = label.texture_size[0]
