from kivy.graphics import Callback
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.gridlayout import GridLayout

from dataFunctions import select_grid_values
from functions import text_color, background_color
from myButton import MyButtonBorder


class DBGrid(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_values = []
        self.size_hint = (None, None)
        self.row_height = 32
        self.title = []
        self.canvas.add(Callback(self.update_grid))
        self.titleGrid = None
        self.blank_button = None
        self.scroll_bar = None

    def get_values(self, fields, sql, params=""):
        self.clear_widgets()
        values = select_grid_values(sql, params)
        self.title = fields
        self.cols = len(fields)
        for v in values:
            values = []
            for i in range(len(v)):
                values.append(str(v[i]))
            self.row_values.append(values)

        j = 0
        if self.titleGrid:
            self.titleGrid.cols = len(self.title) - 1
            self.titleGrid.clear_widgets()
            for title in self.title:
                if j > 0:
                    self.titleGrid.add_widget(TitleButton(-1, j, text=title))
                j += 1

        i = 0
        for row in self.row_values:
            j = 0
            for value in row:
                self.add_widget(GridButton(i, j, text=value, height=self.row_height))
                j += 1
            i += 1

        self.height = len(self.row_values) * self.row_height

    def update_grid(self, _instr=None):
        grid_width = 0
        if self.scroll_bar:
            if (not self.blank_button) and self.titleGrid:
                self.titleGrid.cols += 1
                j = self.titleGrid.cols
                self.blank_button = TitleButton(-1, j, text=' ')
                self.blank_button.width = self.scroll_bar.width
                self.titleGrid.add_widget(self.blank_button)
        elif self.blank_button:
            self.titleGrid.remove_widget(self.blank_button)

        if self.cols > 2 and not self.size_hint_x:
            for i in range(len(self.title)):
                if i > 0:
                    max_width = 0
                    for btn in self.children:
                        if (btn.col_index == i) and (btn.texture_size[0] > max_width):
                            max_width = btn.texture_size[0]

                    if self.titleGrid:
                        for btn in self.titleGrid.children:
                            if (btn.col_index == i) and (btn.texture_size[0] > max_width):
                                max_width = btn.texture_size[0]

                    max_width += 8  # left + right padding

                    for btn in self.children:
                        if (btn.col_index == i) and (btn.width < max_width):
                            btn.width = max_width

                    if self.titleGrid:
                        for btn in self.titleGrid.children:
                            if (btn.col_index == i) and (btn.width < max_width):
                                btn.width = max_width

                    grid_width += max_width
            self.width = grid_width
        else:
            for btn in self.children:
                if btn.col_index == 1:
                    btn.width = self.width

        self.canvas.ask_update()

    def add_row(self, row_values):
        j = 0
        row_count = len(self.children) // 2
        for r in row_values:
            self.add_widget(GridButton(row_count, j, text=r, height=self.row_height))
            j += 1

    def get_selected_id(self):
        return self.get_selected_field(0)

    def get_selected_field(self, col_index=0):
        for btn in self.children:
            if isinstance(btn, GridButton) and btn.state == 'down' and btn.col_index == col_index:
                return btn.text


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
