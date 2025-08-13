from os.path import isfile

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from dbGrid import DBGrid, GridButton
from gridContainer import GridContainer
from myButton import MyButtonBorder
from myPopup import MessageBox


class FileGrid(BoxLayout):

    def __init__(self, input_widget, **kwargs):
        super().__init__(**kwargs)
        self.grid = DBGrid()
        self.input_widget = input_widget
        file_grid = GridContainer(grid=self.grid, has_title=False)
        file_grid.container.size_hint = (1, 1)
        self.grid.size_hint = (1, None)
        file_grid.padding = 2

        self.orientation = 'horizontal'
        self.add_widget(file_grid)

        box_buttons = GridLayout(rows=3, cols=1, size_hint=(None, 1), width=108,
                                 padding=[6, 2, 2, 2])

        action_buttons = [MyButtonBorder(text=_("Add")), MyButtonBorder(text=_("Del")),
                          MyButtonBorder(text=_("Clear"))]
        for b in action_buttons:
            b.size_hint = (None, None)
            b.width = 100
            b.height = 30
            box_buttons.add_widget(b)

        action_buttons[0].bind(on_release=self.btn_add_onrelease)
        action_buttons[1].bind(on_release=self.btn_del_onrelease)
        action_buttons[2].bind(on_release=self.btn_clear_onrelease)
        self.add_widget(box_buttons)

    def refresh_file_list(self, index):
        params = [index]
        if self.grid:
            self.grid.get_values(['id', 'Filename'],
                                 """SELECT id,file FROM FILES WHERE gameid=?""", params)

    def add_value(self, value):
        tmp_id = len(self.grid.children) // 2
        self.grid.add_row([str(tmp_id), value])
        self.input_widget.text = ''

    def btn_add_onrelease(self, _widget):
        if self.input_widget:
            value = self.input_widget.text
            if isfile(value):
                self.add_value(value)
            else:
                MessageBox().alert(_('File not found!'))

    def btn_del_onrelease(self, _widget):
        values = []
        for c in self.grid.children:
            if isinstance(c, GridButton) and c.state == "normal":
                values.append(c.text)
        self.grid.clear_widgets()
        for i in range(0, len(values) - 1, 2):
            self.add_value(values[i])

    def btn_clear_onrelease(self, _widget):
        self.grid.clear_widgets()

    def get_all_files(self):
        files = []
        if len(self.grid.children) > 0:
            for i in range(len(self.grid.children) - 2, -1, -2):
                files.append(self.grid.children[i].text)
        return files
