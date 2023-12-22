from kivy.core.window import Window

from dbGrid import DBGrid
from frmGames import FrmGames
from gridContainer import GridContainer
from myPopup import ModalWindow, MyPopup


class FrmManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)

        self.grid = DBGrid()
        self.topGrid = GridContainer(grid=self.grid, has_title=True)
        self.add_widget(self.topGrid)
        self.grid.get_values(['id', 'Name', 'Tab', 'Mod Group'],
                             """SELECT g.id, g.name, t.label, r.groupname FROM gamedef g 
                             LEFT JOIN tabs t ON g.tabindex=t.tabindex
                             LEFT JOIN groups r ON g.modgroup=r.id""")

        self.CreateBoxButtons('Delete', 'Close')
        self.btnEdit = self.AddButon('Edit')
        self.btnAdd = self.AddButon('Add')
        if self.grid.children[0].row_index > 0:
            self.topGrid.select_index(0)
        self.dialog.size = Window.size
        self.popup = MyPopup()
        self.btnAdd.bind(on_release=self.btnAdd_on_press)

    def btnAdd_on_press(self, widget):
        self.popup.content = FrmGames(self.popup)
        self.popup.open()
