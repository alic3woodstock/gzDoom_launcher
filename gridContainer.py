from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView

from myLayout import MyBoxLayout
from scrollBar import VertScrollBar


class GridContainer(AnchorLayout):
    def __init__(self, grid, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.padding = 16

        self.container = MyBoxLayout()
        self.container.lineWidth = 1
        self.container.size_hint = (None, 1)

        self.scroll = ScrollView()
        self.scroll.scroll_type = ['bars']
        self.scroll.always_overscroll = False
        self.scroll.bar_width = 4
        self.grid = grid
        self.row_height = 32

        self.scroll.add_widget(self.grid)
        self.container.add_widget(self.scroll)
        self.add_widget(self.container)
        self.canvas.add(Callback(self.scroll_update))

    def scroll_update(self, instr):
        scroll = None
        for widget in self.container.children:
            if isinstance(widget, VertScrollBar):
                scroll = widget
                break

        if self.scroll.viewport_size[1] > self.scroll.height:
            if not scroll:
                self.container.add_widget(VertScrollBar(self.scroll))

        elif scroll:
            self.container.remove_widget(scroll)

        if scroll:
            self.container.width = self.grid.width + scroll.width
        else:
            self.container.width = self.grid.width


    def get_index(self):
        if len(self.grid.children) > 0:
            for i in range(len(self.grid.children)):
                if self.grid.children[i].state == 'down':
                    return len(self.grid.children) - 1 - (i // self.grid.cols)
                i += self.grid.cols

    def select_index(self, index):
        index = len(self.grid.children) - 1 - index
        index = index * self.grid.cols
        if index < len(self.grid.children) and index >= 0:
            self.grid.children[index].state = 'down'

    def load_next(self):
        index = self.get_index()
        if index < (len(self.grid.children)):
            self.select_index(index + 1)

    def load_previous(self):
        index = self.get_index()
        if index > 0:
            self.select_index(index - 1)

    def page_down(self):
        sBottom = self.scroll.viewport_size[1] / self.row_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / self.row_height)
        if sBottom <= 0:
            self.select_index(len(self.grid.children) - 1)
        else:
            index = self.get_index()
            index2 = len(self.grid.children) - sBottom - 1
            print(index, index2)
            if index == index2:
                if (sBottom < qtdByView):
                    self.select_index(len(self.grid.children) - 1)
                else:
                    self.select_index(index + qtdByView)
            else:
                self.select_index(index2)

    def page_up(self):
        sBottom = self.scroll.viewport_size[1] / self.row_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / self.row_height)
        sTop = len(self.grid.children) - sBottom - qtdByView
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

