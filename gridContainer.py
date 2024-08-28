from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from myLayout import MyBoxLayout
from scrollBar import VertScrollBar


class GridContainer(AnchorLayout):
    def __init__(self, grid, has_title=False, anchor_x='center', **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = anchor_x
        self.padding = 16

        self.container = MyBoxLayout()
        self.container.lineWidth = 1
        self.container.size_hint = (None, 1)

        self.scroll = ScrollView()
        self.scroll.scroll_type = ['bars']
        self.scroll.always_overscroll = False
        self.scroll.bar_width = 4
        grid.scroll = self.scroll
        self.grid = grid

        if has_title:
            self.outsideBox = BoxLayout()
            self.outsideBox.orientation = 'vertical'
            self.outsideBox.size_hint = (None, 1)
            self.titleBar = MyBoxLayout()
            self.titleBar.borders = ['top', 'left', 'right']
            self.titleBar.lineWidth = 1
            self.titleBar.size_hint = (1, None)
            self.titleBar.height = grid.row_height
            title_grid = GridLayout()
            grid.titleGrid = title_grid
            self.titleBar.height = grid.row_height
            self.titleBar.add_widget(title_grid)
            self.outsideBox.add_widget(self.titleBar)
            self.outsideBox.add_widget(self.container)
            self.add_widget(self.outsideBox)
        else:
            self.add_widget(self.container)
        self.has_title = has_title
        self.scroll.add_widget(self.grid)
        self.container.add_widget(self.scroll)
        self.canvas.add(Callback(self.scroll_update))

    def scroll_update(self, _instr):
        scroll = None
        for widget in self.container.children:
            if isinstance(widget, VertScrollBar):
                scroll = widget
                break

        if self.scroll.viewport_size[1] > self.scroll.height:
            if not scroll:
                self.grid.scroll_bar = VertScrollBar(self.scroll)
                self.container.add_widget(self.grid.scroll_bar)
        elif scroll:
            self.container.remove_widget(scroll)
            self.grid.scroll_bar = None

        if scroll:
            self.container.width = self.grid.width + scroll.width
        else:
            self.container.width = self.grid.width

        if self.has_title:
            self.outsideBox.width = self.container.width

    def get_index(self):
        if len(self.grid.children) > 0:
            for btn in self.grid.children:
                if btn.state == 'down':
                    return btn.row_index
        return 0

    def select_index(self, index):
        if len(self.grid.children) > 0:
            for btn in self.grid.children:
                if btn.row_index == index:
                    btn.state = 'down'
                    return

    def load_next(self):
        index = self.get_index()
        if index < (len(self.grid.children)):
            self.select_index(index + 1)

    def load_previous(self):
        index = self.get_index()
        if index > 0:
            self.select_index(index - 1)

    def page_down(self):
        last_item = len(self.grid.children) // self.grid.cols - 1
        s_bottom = self.scroll.viewport_size[1] / self.grid.row_height
        s_bottom = round(self.scroll.vbar[0] * s_bottom)
        qtd_by_view = round(self.scroll.height / self.grid.row_height)
        if s_bottom <= 0:
            self.select_index(last_item)
        else:
            index = self.get_index()
            index2 = last_item - s_bottom
            if index == index2:
                if s_bottom < qtd_by_view:
                    self.select_index(last_item)
                else:
                    self.select_index(index + qtd_by_view)
            else:
                self.select_index(index2)

    def page_up(self):
        s_bottom = self.scroll.viewport_size[1] / self.grid.row_height
        s_bottom = round(self.scroll.vbar[0] * s_bottom)
        qtd_by_view = round(self.scroll.height / self.grid.row_height)
        s_top = len(self.grid.children) // self.grid.cols - s_bottom - qtd_by_view
        if s_top <= 0:
            self.select_index(0)
        else:
            index = self.get_index()
            if index == s_top:
                if s_top >= qtd_by_view:
                    self.select_index(s_top - qtd_by_view)
                else:
                    self.select_index(0)
            else:
                self.select_index(s_top)
