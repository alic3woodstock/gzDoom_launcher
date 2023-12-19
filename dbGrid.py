from kivy.graphics import Callback
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.gridlayout import GridLayout

from gameDefDb import GameDefDb
from myButton import MyButtonBorder, background_color, text_color


class DBGrid(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_values = []
        self.size_hint = (None, None)
        self.row_height = 32
        self.title = []
        self.canvas.add(Callback(self.update_grid))
        self.titleGrid = None

    def get_values(self, fields, sql):
        gameDefDb = GameDefDb()
        values = gameDefDb.SelectGridValues(sql)
        self.title = fields
        self.cols = len(fields)
        for v in values:
            values = []
            for i in range(len(v)):
                values.append(str(v[i]))
            self.row_values.append(values)

        j = 0
        self.titleGrid.cols = len(self.title) - 1
        self.titleGrid.clear_widgets()
        for title in self.title:
            if j > 0:
                self.titleGrid.add_widget(TitleButton(-1, j, text=title))
            j += 1

        if self.scroll:
            self.titleGrid.cols += 1
            blankButton = TitleButton(0, j, text='')
            blankButton.size_hint = (1, 1)
            self.titleGrid.add_widget(blankButton)

        i = 0
        for row in self.row_values:
            j = 0
            for value in row:
                self.add_widget(GridButton(i, j, text=value, height=self.row_height))
                j += 1
            i += 1

        self.height = len(self.row_values) * self.row_height

    def update_grid(self, instr):
        grid_width = 0
        for i in range(len(self.title)):
            if i > 0:
                max_width = 0
                for btn in self.children:
                    if (btn.col_index == i) and (btn.texture_size[0] > max_width):
                        max_width = btn.texture_size[0]

                for btn in self.titleGrid.children:
                    if (btn.col_index == i) and (btn.texture_size[0] > max_width):
                        max_width = btn.texture_size[0]

                max_width += 8  # left + right padding

                for btn in self.children:
                    if (btn.col_index == i) and (btn.width < max_width):
                        btn.width = max_width

                for btn in self.titleGrid.children:
                    if (btn.col_index == i) and (btn.width < max_width):
                        btn.width = max_width

                grid_width += max_width

        self.width = grid_width
        self.canvas.ask_update()


class GridButton(ToggleButtonBehavior, MyButtonBorder):

    def __init__(self, row_index, col_index, **kwargs):
        super().__init__(**kwargs)
        self.row_index = row_index
        self.col_index = col_index
        self.size_hint = (None, None)
        self.width = 0

    def on_state(self, widget, value):
        if value == 'down':
            for btn in self.parent.children:
                if (btn != widget) and isinstance(btn, GridButton):
                    if btn.row_index == widget.row_index:
                        btn.state = widget.state
                        scroll = self.parent.scroll
                        if scroll:
                            scroll.scroll_to(widget, padding=0)
                    else:
                        btn.state = 'normal'

    def on_press(self):
        if self.state == 'normal':
            self.state = 'down'


class TitleButton(MyButtonBorder):

    def __init__(self, row_index, col_index, **kwargs):
        super().__init__(**kwargs)
        self.row_index = row_index
        self.col_index = col_index
        self.size_hint = (None, 1)
        self.width = 0
        self.background_color = text_color
        self.highlight_color = text_color
        self.text_color = background_color
        self.border_color = background_color
