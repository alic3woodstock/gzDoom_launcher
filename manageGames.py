from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout

from gameGrid import GameGrid
from myButton import MyButtonBorder
from myPopup import ModalWindow

class ManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size

        self.topLayout = BoxLayout()
        self.topLayout.padding = 16
        self.grid = GameGrid()

        self.add_widget(self.topLayout)
        self.CreateBoxButtons('Delete', 'Close')
        self.btnEdit = self.AddButon('Edit')
        self.btnAdd = self.AddButon('Add')
