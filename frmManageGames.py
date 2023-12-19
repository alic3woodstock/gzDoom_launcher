from kivy.core.window import Window
from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView

from dbGrid import DBGrid
from myLayout import MyBoxLayout
from myPopup import ModalWindow
from scrollBar import VertScrollBar
from gridContainer import GridContainer


class FrmManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size

        self.grid = DBGrid()
        self.topLayout = GridContainer(grid=self.grid, has_title=True)
        self.add_widget(self.topLayout)
        self.grid.get_values(['id','Name', 'Tab', 'Mod Group'],
                             """SELECT g.id, g.name, t.label, r.groupname FROM gamedef g 
                             LEFT JOIN tabs t ON g.tabindex=t.tabindex
                             LEFT JOIN groups r ON g.modgroup=r.id""")

        self.CreateBoxButtons('Delete', 'Close')
        self.btnEdit = self.AddButon('Edit')
        self.btnAdd = self.AddButon('Add')
        if self.grid.children[0].row_index > 0:
            self.topLayout.select_index(0)
