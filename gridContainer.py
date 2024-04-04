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
            titleGrid = GridLayout()
            grid.titleGrid = titleGrid
            self.titleBar.height = grid.row_height
            self.titleBar.add_widget(titleGrid)
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
        lastItem = len(self.grid.children) // self.grid.cols - 1
        sBottom = self.scroll.viewport_size[1] / self.grid.row_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / self.grid.row_height)
        if sBottom <= 0:
            self.select_index(lastItem)
        else:
            index = self.get_index()
            index2 = lastItem - sBottom
            if index == index2:
                if sBottom < qtdByView:
                    self.select_index(lastItem)
                else:
                    self.select_index(index + qtdByView)
            else:
                self.select_index(index2)

    def page_up(self):
        sBottom = self.scroll.viewport_size[1] / self.grid.row_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / self.grid.row_height)
        sTop = len(self.grid.children) // self.grid.cols - sBottom - qtdByView
        if sTop <= 0:
            self.select_index(0)
        else:
            index = self.get_index()
            if index == sTop:
                if sTop >= qtdByView:
                    self.select_index(sTop - qtdByView)
                else:
                    self.select_index(0)
            else:
                self.select_index(sTop)
