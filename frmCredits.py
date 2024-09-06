from kivy.core.window import Window
from kivy.metrics import Metrics
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label

from credits import Credits
from genericForm import GenericForm
from myButton import HTMLButton
from myPopup import MyPopup, ModalWindow


class FrmCredits(ModalWindow):
    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()

        self.genericForm = GenericForm()
        self.genericForm.topLayout.cols = 1
        self.genericForm.children_height = self.genericForm.children_height / 2

        credit_list = []
        for i in range(0, 29):
            credit_list.append(Credits(i))

        self.html_buttons = []
        for c in credit_list:
            self.genericForm.topLayout.add_widget(Label(text='[color=ff0000]' + c.name + '[/color]',
                                                        markup=True))
            self.genericForm.topLayout.add_widget(Label(text=c.author))
            anchor = AnchorLayout()
            anchor.size_hint = (1, None)
            anchor.height = 42
            anchor.anchor_y = 'top'
            button = HTMLButton(url=c.url)
            button.size_hint = (1, None)
            button.height = self.genericForm.children_height
            self.html_buttons.append(button)
            anchor.add_widget(button)
            self.genericForm.topLayout.add_widget(anchor)

        self.add_widget(self.genericForm)

        self.create_box_buttons(
            '', 'Ok')
        self.dialog.height = Window.height
        Window.bind(mouse_pos=self.mouse_pos)

    def mouse_pos(self, *args):
        pos = args[1]
        x = pos[0] * Metrics.dpi / 96
        y = pos[1] * Metrics.dpi / 96
        pos = (x, y)
        collide = False
        for b in self.html_buttons:
            if b.collide_point(*b.to_widget(x, y)):
                collide = True
                break
        if collide:
            Window.set_system_cursor('hand')
        else:
            Window.set_system_cursor('arrow')
