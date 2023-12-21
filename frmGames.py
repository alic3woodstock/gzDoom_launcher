from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

from genericForm import GenericForm
from myPopup import ModalWindow


class FrmGames(ModalWindow):

    def __init__(self, dialog, game=None, **kwargs):
        super().__init__(dialog, **kwargs)

        self.formLayout = GenericForm()
        self.formLayout.add_text_field(text='Name:', field_name='name')
        self.formLayout.add_checkbox(text='Is a Mod', field_name='ismod')
        self.formLayout.add_dropdown(text='Tab.:', field_name='tab')
        self.formLayout.add_text_field(text='Game Exec.:', field_name='gamexec')
        self.add_widget(self.formLayout)

        self.CreateBoxButtons('OK', 'Cancel')
        self.game = game
        self.dialog.size = Window.size
