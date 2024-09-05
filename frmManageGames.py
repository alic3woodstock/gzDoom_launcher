from kivy.core.window import Window
from dbGrid import DBGrid
from frmGames import FrmGames
from gameDefDB import delete_game_by_id, select_game_by_id
from gridContainer import GridContainer
from myPopup import ModalWindow, MyPopup, Dialog

refresh_database = False


class FrmManageGames(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.dialog.height = Window.height
        self.popup = MyPopup()
        self.popup.bind(on_dismiss=self.popup_dismiss)
        self.grid = None
        self.topGrid = None
        self.btnEdit = None
        self.btnAdd = None
        self.create_grid()

    def btn_add_on_press(self, _widget):
        self.popup.content = FrmGames(self.popup)
        self.popup.open()

    def btn_edit_on_press(self, _widget):
        game = select_game_by_id(self.grid.get_selected_id())
        self.popup.content = FrmGames(self.popup, game)
        self.popup.open()

    def btn_delete_on_press(self, _widget):
        game = self.grid.get_selected_field(1)
        dialog = Dialog(self.popup, "Delete game " + str(game) + "?", txt_ok="Yes",
                        txt_cancel="No", icon="question")
        self.popup.content = dialog
        dialog.btnOk.bind(on_release=self.btn_delete_on_click)
        self.popup.open()

    def btn_delete_on_click(self, _widget):
        delete_game_by_id(self.grid.get_selected_id())
        global refresh_database
        refresh_database = True
        self.popup.dismiss()

    def popup_dismiss(self, _widget):
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
        self.create_box_buttons('Delete', 'Close')
        self.btnEdit = self.add_buton('Edit')
        self.btnAdd = self.add_buton('Add')
        if len(self.grid.children) and self.grid.children[0].row_index > 0:
            self.topGrid.select_index(0)
        self.btnAdd.bind(on_release=self.btn_add_on_press)
        self.btnOk.bind(on_release=self.btn_delete_on_press)
        self.btnEdit.bind(on_release=self.btn_edit_on_press)
