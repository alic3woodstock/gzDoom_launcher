import frmManageGames
from os.path import isfile
from kivy.core.window import Window
from gameDef import GameDef
from createDB import CreateDB
from gameDefDB import insert_game, update_game, update_last_run_mod
from gameTabDB import select_all_game_tab_configs
from genericForm import GenericForm
from groupDB import select_all_groups
from myButton import DropDownItem
from myPopup import ModalWindow
from myPopup import MyPopup, MessageBox, Dialog


class FrmGames(ModalWindow):

    def __init__(self, dialog, game=None, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()

        self.formLayout = GenericForm()
        self.formLayout.add_text_field(text='Name:', field_name='name')
        self.formLayout.add_checkbox(text='Is a Mod', field_name='ismod')
        self.formLayout.add_dropdown(text='Tab.:', field_name='tab')
        self.formLayout.add_file_field(text='Game Exec.:', field_name='gamexec')
        self.formLayout.add_dropdown(text='Mod Group:', field_name='modgroup')
        self.formLayout.add_file_field(text='Wad:', field_name='wad')
        self.formLayout.add_text_field(text='Cmd. Parameters:', field_name='params')
        self.formLayout.add_file_field(text='Files:', field_name='files')
        self.formLayout.add_file_list(self.formLayout.ids.files,
                                      field_name='filelist')
        self.formLayout.ids.filelist.refresh_file_list(-1)
        self.formLayout.link_file_list('filelist', 'files')
        self.add_widget(self.formLayout)

        game_data = CreateDB()
        tabs = select_all_game_tab_configs()
        dropdown = self.formLayout.ids.tab
        for t in tabs:
            btnTab = DropDownItem(game=t, text=t.name)
            dropdown.add_widget(btnTab)
        dropdown.select(tabs[0])

        groups = select_all_groups()
        dropdown = self.formLayout.ids.modgroup
        for g in groups:
            btnGroup = DropDownItem(game=g, text=g.name)
            dropdown.add_widget(btnGroup)
        dropdown.select(groups[0])

        self.CreateBoxButtons(
            'OK', 'Cancel')
        self.game = game
        self.dialog.size = Window.size
        self.btnOk.bind(on_release=self.btnok_on_release)
        if game:
            self.load_game()

    def btnok_on_release(self, _widget):
        # AddGame
        if self.formLayout.ids.ismod.active:
            tab = -1
        else:
            tab = self.formLayout.ids.tab.main_button.game.index

        if self.game:
            gameId = self.game.id
        else:
            gameId = 0

        gameDef = GameDef(gameId,
                          self.formLayout.ids.name.text.strip(),
                          tab,
                          self.formLayout.ids.gamexec.text.strip(),
                          self.formLayout.ids.modgroup.main_button.game.id,
                          0,
                          self.formLayout.ids.wad.text.strip(),
                          self.formLayout.ids.filelist.get_all_files(),
                          self.formLayout.ids.params.text.strip())

        msg = MessageBox()

        if not gameDef.name:
            msg.alert('Invalid name!')
        elif not isfile(gameDef.exec):
            msg.alert('Invalid game executable!')
        elif gameDef.iWad and not isfile(gameDef.iWad):
            msg.alert('Invalid game wad!')
        else:
            frmManageGames.refresh_database = True
            if gameId > 0:
                if gameDef.groupId != self.game.groupId:
                    update_last_run_mod(self.game, 0)
                update_game(gameDef, True)
            else:
                insert_game(gameDef)
            self.popup.content = Dialog(self.popup, text="New game/mod successfully added!",
                                        txtCancel="OK")
            self.dialog.dismiss()

    def load_game(self):
        self.formLayout.ids.name.text = self.game.name

        if self.game.tabId < 0:
            self.formLayout.ids.ismod.state = 'down'
        else:
            self.formLayout.ids.tab.select(self.game.tab)

        self.formLayout.ids.gamexec.text = self.game.exec
        self.formLayout.ids.modgroup.select(self.game.group)
        self.formLayout.ids.wad.text = self.game.iWad
        self.formLayout.ids.params.text = self.game.cmdParams

        for f in self.game.files:
            self.formLayout.ids.filelist.add_value(f)
