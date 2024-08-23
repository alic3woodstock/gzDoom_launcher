from os.path import isfile

from kivy.core.window import Window

from genericForm import GenericForm
from myPopup import MyPopup, ModalWindow, MessageBox
from gameDefDB import update_wad
from gameTabDB import select_game_tab_by_id


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

        self.CreateBoxButtons(
            'OK', 'Cancel')
        self.btnOk.bind(on_release=self.btnOk_on_press)
        self.dialog.width = Window.width
        # box buttons height + generic form height for 1 component
        self.dialog.height = 64 + 64 + self.formLayout.padding[0] * 2 + self.formLayout.spacing[0]

    def btnOk_on_press(self, _widget):
        msg = MessageBox()
        file = self.formLayout.ids.file.text
        if not isfile(file):
            msg.alert('Invalid wad file!')
        else:
            update_wad(file, self.mod_group)
            tab = select_game_tab_by_id(1)
            msg.message('Wad ' + self.old_wad + ' successfully replaced by '
                        + self.suggested_wad + ' in tab '
                        + tab.name + "!", icon='information')
            self.dialog.dismiss()