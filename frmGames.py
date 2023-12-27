from kivy.core.window import Window

from gameDefDb import GameDefDb
from genericForm import GenericForm
from myButton import DropDownItem
from myPopup import ModalWindow


class FrmGames(ModalWindow):

    def __init__(self, dialog, game=None, **kwargs):
        super().__init__(dialog, **kwargs)

        self.formLayout = GenericForm()
        self.formLayout.add_text_field(text='Name:', field_name='name')
        self.formLayout.add_checkbox(text='Is a Mod', field_name='ismod')
        self.formLayout.add_dropdown(text='Tab.:', field_name='tab')
        self.formLayout.add_file_field(text='Game Exec.:', field_name='gamexec')
        self.formLayout.add_dropdown(text='Mod Group:', field_name='modgroup' )
        self.formLayout.add_file_field(text='Wad:', field_name='wad')
        self.formLayout.add_text_field(text='Cmd. Parameters:', field_name='params')
        self.formLayout.add_file_field(text='Files', field_name='files')
        self.add_widget(self.formLayout)

        game_data = GameDefDb()
        tabs = game_data.SelectAllGameTabConfigs()
        for t in tabs:
            btnTab = DropDownItem(game=t, text=t.name)
            dropdown = self.formLayout.ids.tab
            dropdown.add_widget(btnTab)
            btnTab.bind(on_release=lambda btn: dropdown.select(t))



        self.CreateBoxButtons(
            'OK', 'Cancel')
        self.game = game
        self.dialog.size = Window.size
