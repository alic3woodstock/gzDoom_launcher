from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from os.path import isfile
from dbGrid import DBGrid
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

        action_buttons = [MyButtonBorder(text="Add"), MyButtonBorder(text="Del"),
                          MyButtonBorder(text="Clear")]
        for b in action_buttons:
            b.size_hint = (None, None)
            b.width = 100
            b.height = 30
            box_buttons.add_widget(b)

        action_buttons[0].bind(on_release=self.btn_add_onrelease)
        self.add_widget(box_buttons)

    def refresh_file_list(self, index):
        params = [index]
        if self.grid:
            self.grid.get_values(['id', 'Filename'],
                                 """SELECT id,file FROM FILES WHERE gameid=?""", params)

    def add_value(self, value):
        if isfile(value):
            self.grid.add_row(['-1', value])
            self.input_widget.text = ''
        else:
            MessageBox().alert('File not found!')

    def btn_add_onrelease(self, _widget):
        if self.input_widget:
            self.add_value(self.input_widget.text)

    def get_all_files(self):
        files = []
        if len(self.grid.children) > 0:
            for i in range(len(self.grid.children) - 2, -1, -2):
                files.append(self.grid.children[i].text)
        return files
