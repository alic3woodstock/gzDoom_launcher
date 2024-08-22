from kivy.core.window import Window

from dbGrid import DBGrid
from frmGames import FrmGames
from gameDefDb import GameDefDb
from gridContainer import GridContainer
from myPopup import ModalWindow, MyPopup, Dialog

refresh_database = False


class FrmManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.size = Window.size
        self.popup = MyPopup()
        self.popup.bind(on_dismiss=lambda f: self.popup_dismiss())
        self.create_grid()

    def btnAdd_on_press(self, _widget):
        self.popup.content = FrmGames(self.popup)
        self.popup.open()

    def btnEdit_on_press(self, _widget):
        gameDefDb = GameDefDb()
        game = gameDefDb.SelectGameById(self.grid.get_selected_id())
        self.popup.content = FrmGames(self.popup, game)
        self.popup.open()

    def btnDelete_on_press(self, _widget):
        game = self.grid.get_selected_field(1)
        dialog = Dialog(self.popup, "Delete game " + str(game) + "?", txtOk="Yes",
                        txtCancel="No", icon="question")
        self.popup.content = dialog
        dialog.btnOk.bind(on_release=self.btnDelete_on_click)
        self.popup.open()

    def btnDelete_on_click(self, _widget):
        gameDefDb = GameDefDb()
        gameDefDb.DeleteGameById(self.grid.get_selected_id())
        global refresh_database
        refresh_database = True
        self.popup.dismiss()

    def popup_dismiss(self):
        global refresh_database
        if refresh_database:
            self.create_grid()
            refresh_database = False

    def create_grid(self):
        self.clear_widgets()
        self.grid = DBGrid()
        self.topGrid = GridContainer(grid=self.grid, has_title=True)
        self.add_widget(self.topGrid)
        self.grid.get_values(['id', 'Name', 'Tab', 'Mod Group'],
                             """SELECT g.id, g.name, t.label, r.groupname
                                    FROM gamedef g 
                                    LEFT JOIN tabs t ON g.tabindex=t.tabindex
                                    LEFT JOIN groups r ON g.modgroup=r.id
                                    order by (CASE WHEN g.tabindex == -1 
                                    THEN 99999 ELSE g.tabindex END), g.name""")
        self.topGrid.scroll.scroll_y = 0
        self.CreateBoxButtons('Delete', 'Close')
        self.btnEdit = self.AddButon('Edit')
        self.btnAdd = self.AddButon('Add')
        if len(self.grid.children) and self.grid.children[0].row_index > 0:
            self.topGrid.select_index(0)
        self.btnAdd.bind(on_release=self.btnAdd_on_press)
        self.btnOk.bind(on_release=self.btnDelete_on_press)
        self.btnEdit.bind(on_release=self.btnEdit_on_press)
