from os.path import isfile, basename

from kivy.core.window import Window

from functions import button_height
from gameDefDB import update_wad
from gameTabDB import select_game_tab_by_id
from genericForm import GenericForm
from myPopup import MyPopup, ModalWindow, MessageBox


class FrmReplaceWad(ModalWindow):

    def __init__(self, dialog, mod_group=1, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()
        if mod_group == 2:
            self.old_wad = 'blasphem.wad'
            self.suggested_wad = 'heretic.wad'
        else:
            self.old_wad = 'freedoom2.wad'
            self.suggested_wad = 'doom2.wad'
        self.mod_group = mod_group
        self.formLayout = GenericForm()
        text = 'Replace by (' + self.suggested_wad + '):'
        self.formLayout.add_file_field(text, 'file')
        self.add_widget(self.formLayout)

        self.create_box_buttons(
            'OK', 'Cancel')
        self.btnOk.bind(on_release=self.btn_ok_on_press)
        self.dialog.height = (button_height * 2  # box buttons height + tithe height
                              + self.formLayout.get_height())

    def btn_ok_on_press(self, _widget):
        msg = MessageBox()
        file = self.formLayout.ids.file.text
        if not isfile(file):
            msg.alert('Invalid wad file!')
        else:
            update_wad(file, self.mod_group)
            tab = select_game_tab_by_id(1)
            msg.message('Wad ' + self.old_wad + ' successfully replaced by '
                        + basename(file) + ' in tab '
                        + tab.name + "!", icon='information')
            self.dialog.dismiss()
