from os.path import isfile

from kivy.core.window import Window

import frmManageGames
from gameDef import GameDef
from gameDefDB import insert_game, update_game, update_last_run_mod
from gameTabDB import select_all_game_tabs
from genericForm import GenericForm
from groupDB import select_all_groups
from myButton import DropDownItem
from myPopup import ModalWindow
from myPopup import MyPopup, MessageBox, Dialog


def get_widget_index(widget):
    for i in range(len(widget.parent.children) - 1, 0, -1):
        if widget.parent.children[i] == widget:
            return i


class FrmGames(ModalWindow):

    def __init__(self, dialog, game=None, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()

        self.genericForm = GenericForm()
        self.genericForm.add_text_field(text='Name:', field_name='name')
        self.genericForm.add_checkbox_field(text='Is a Mod', field_name='ismod')
        self.genericForm.add_file_field(text='Game Exec.:', field_name='gamexec')
        self.genericForm.add_file_field(text='Wad:', field_name='wad')
        self.genericForm.add_dropdown(text='Tab.:', field_name='tab')
        self.genericForm.add_dropdown(text='Mod Group:', field_name='modgroup')
        self.genericForm.add_text_field(text='Cmd. Parameters:', field_name='params')
        self.genericForm.add_file_field(text='Files:', field_name='files')
        self.genericForm.add_file_list(self.genericForm.ids.files,
                                       field_name='filelist')
        self.genericForm.ids.filelist.refresh_file_list(-1)
        self.genericForm.link_file_list('filelist', 'files')
        self.add_widget(self.genericForm)
        self.ismod_index = get_widget_index(self.genericForm.ids.ismod)

        tabs = select_all_game_tabs()
        dropdown = self.genericForm.ids.tab
        for t in tabs:
            btn_tab = DropDownItem(game=t, text=t.name)
            dropdown.add_widget(btn_tab)
        dropdown.select(tabs[0])

        groups = select_all_groups()
        dropdown = self.genericForm.ids.modgroup
        for g in groups:
            btn_group = DropDownItem(game=g, text=g.name)
            dropdown.add_widget(btn_group)
        dropdown.select(groups[0])

        self.create_box_buttons(
            'OK', 'Cancel')
        self.game = game
        self.dialog.size = Window.size
        self.btnOk.bind(on_release=self.btnok_on_release)
        self.genericForm.ids.ismod.button.bind(on_release=self.ismod_on_release)

        if game:
            self.load_game()

    def btnok_on_release(self, _widget):
        # AddGame
        if self.game:
            game_id = self.game.id
        else:
            game_id = 0

        game_def = GameDef(game_id,
                           self.genericForm.ids.name.text.strip(),
                           self.genericForm.ids.tab.main_button.game.index,
                           self.genericForm.ids.gamexec.text.strip(),
                           self.genericForm.ids.modgroup.main_button.game.id,
                           0,
                           self.genericForm.ids.wad.text.strip(),
                           self.genericForm.ids.filelist.get_all_files(),
                           self.genericForm.ids.params.text.strip())

        if self.genericForm.ids.ismod.active:
            game_def.tabId = -1
            game_def.exec = ''
            game_def.iWad = ''

        msg = MessageBox()

        if not game_def.name:
            msg.alert('Invalid name!')
        elif game_def.tabId >= 0 and not isfile(game_def.exec):
            msg.alert('Invalid game executable!')
        elif game_def.iWad and not isfile(game_def.iWad):
            msg.alert('Invalid game wad!')
        else:
            frmManageGames.refresh_database = True
            if game_id > 0:
                if game_def.groupId != self.game.groupId:
                    update_last_run_mod(self.game, 0)
                update_game(game_def, True)
            else:
                insert_game(game_def)
            self.popup.content = Dialog(self.popup, text="New game/mod successfully added!",
                                        txt_cancel="OK")
            self.dialog.dismiss()

    def load_game(self):
        self.genericForm.ids.name.text = self.game.name

        if self.game.tabId < 0:
            self.genericForm.ids.ismod.active = True
            self.genericForm.hide_field('gamexec', True)
            self.genericForm.hide_field('wad', True)
            self.genericForm.hide_field('tab', True)
            self.ismod_index = get_widget_index(self.genericForm.ids.ismod)
        else:
            self.genericForm.ids.tab.select(self.game.tab)
            self.genericForm.ids.gamexec.text = self.game.exec
            self.genericForm.ids.wad.text = self.game.iWad

        self.genericForm.ids.modgroup.select(self.game.group)
        self.genericForm.ids.params.text = self.game.cmdParams

        for f in self.game.files:
            self.genericForm.ids.filelist.add_value(f)

    def ismod_on_release(self, widget):
        self.genericForm.hide_field('gamexec', widget.active, self.ismod_index)
        self.genericForm.hide_field('wad', widget.active, self.ismod_index)
        self.genericForm.hide_field('tab', widget.active, self.ismod_index)
        if widget.active:
            self.ismod_index = get_widget_index(self.genericForm.ids.ismod)
