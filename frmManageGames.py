from kivy.core.window import Window

from dbGrid import DBGrid
from gridContainer import GridContainer
from myPopup import ModalWindow


class FrmManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size

        self.grid = DBGrid()
        self.topLayout = GridContainer(grid=self.grid, has_title=True)
        self.add_widget(self.topLayout)
        self.grid.get_values(['id', 'Name', 'Tab', 'Mod Group'],
                             """SELECT g.id, g.name, t.label, r.groupname FROM gamedef g 
                             LEFT JOIN tabs t ON g.tabindex=t.tabindex
                             LEFT JOIN groups r ON g.modgroup=r.id""")

        self.CreateBoxButtons('Delete', 'Close')
        self.btnEdit = self.AddButon('Edit')
        self.btnAdd = self.AddButon('Add')
        if self.grid.children[0].row_index > 0:
            self.topLayout.select_index(0)
