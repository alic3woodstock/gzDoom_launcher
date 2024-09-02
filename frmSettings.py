from kivy.core.window import Window
from kivy.graphics import Callback
from kivy.uix.label import Label

from configDB import read_config, write_config
from functions import button_height
from gameTab import GameTab
from gameTabDB import select_all_game_tabs, update_all_game_tabs
from genericForm import GenericForm
from myButton import MyCheckBox
from myLayout import MyAnchorLayout
from myPopup import ModalWindow, MessageBox


class FrmSettings(ModalWindow):
    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.genericForm = GenericForm()

        layout1 = self.anchor_layout()
        layout1.borders = []
        self.label_tabs = Label(text='Configure Tabs:')
        self.label_tabs.size_hint = (None, None)
        self.label_tabs.halign = 'left'
        self.label_tabs.valign = 'middle'
        self.label_tabs.height = self.genericForm.children_height
        layout1.add_widget(self.label_tabs)

        self.genericForm.padding = [16, 0, 16, 16]
        for i in range(1, 10):
            field_name = 'tab' + str(i)
            text = 'Tab ' + str(i) + ':'
            self.genericForm.add_checkbox_input(text, field_name)

        game_tabs = select_all_game_tabs()
        for g in game_tabs:
            if g.index >= 0:
                field_name = 'tab' + str(g.index + 1) + '_check'
                self.genericForm.ids[field_name].active = g.is_enabled
                field_name = 'tab' + str(g.index + 1) + '_name'
                self.genericForm.ids[field_name].text = g.name

        layout2 = self.anchor_layout()
        layout2.borders = ['top']
        layout2.height += 16
        self.ChkCheckUpdate = MyCheckBox(text='Check for GZDoom updates on startup')
        self.ChkCheckUpdate.height = self.genericForm.children_height
        self.ChkCheckUpdate.active = read_config('checkupdate', 'bool')
        layout2.add_widget(self.ChkCheckUpdate)

        self.add_widget(layout1)
        self.add_widget(self.genericForm)
        self.add_widget(layout2)

        self.create_box_buttons(
            'OK', 'Cancel')
        self.btnOk.bind(on_release=self.btn_ok_on_press)

        self.dialog.size = Window.size
        self.dialog.height = (button_height * 2  # box buttons height + tithe height
                              + self.genericForm.get_height()
                              + layout1.height + layout2.height)
        self.canvas.add(Callback(self.update_form))

    def update_form(self, _instr):
        self.label_tabs.size = self.label_tabs.texture_size
        self.ChkCheckUpdate.width = (self.ChkCheckUpdate.label.texture_size[0]
                                     + self.ChkCheckUpdate.box1.width)

    def anchor_layout(self):
        layout = MyAnchorLayout()
        layout.size_hint = (1, None)
        layout.padding = 16
        layout.spacing = self.genericForm.spacing[0]
        layout.height = self.genericForm.children_height
        layout.anchor_x = 'left'
        layout.anchor_y = 'center'
        return layout

    def btn_ok_on_press(self, _widget):
        has_active_tab = False
        empty_text = False
        for i in range(1, 10):
            if self.genericForm.ids['tab' + str(i) + '_check'].active:
                has_active_tab = True
            if (self.genericForm.ids['tab' + str(i) + '_check'].active
                    and not self.genericForm.ids['tab' + str(i) + '_name'].text.strip()):
                empty_text = True

        msg = MessageBox()
        if not has_active_tab:
            msg.alert('At least one tab has to be enabled!')
        elif empty_text:
            msg.alert('Enabled tabs must have a description!')
        else:
            game_tabs = []
            for i in range(0, 9):
                index = i
                name = self.genericForm.ids['tab' + str(i + 1) + '_name'].text.strip()
                is_enabled = self.genericForm.ids['tab' + str(i + 1) + '_check'].active
                game_tabs.append(GameTab(index, name, is_enabled))

            update_all_game_tabs(game_tabs)
            write_config('checkupdate', self.ChkCheckUpdate.active, 'bool')
            self.dialog.dismiss()
