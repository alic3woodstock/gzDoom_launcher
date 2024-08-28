import os
import string

from dbGrid import DBGrid
from myButton import MyToggleButton

if os.name == 'nt':
    from ctypes import windll


class LocalDriveGrid(DBGrid):

    def __init__(self, file_chooser=None, **kwargs):
        super().__init__(**kwargs)
        self.file_chooser = file_chooser

    def get_values(self, **kwargs):
        self.cols = 1
        if os.name == 'nt':
            drives = []
            bitmask = windll.kernel32.GetLogicalDrives()
            for letter in string.ascii_uppercase:
                if bitmask & 1:
                    drives.append(letter)
                bitmask >>= 1

            i = 0
            for letter in drives:
                if os.path.exists(letter + ':\\'):
                    btn_letter = GridButton(i, 0, text=letter + ':')
                    btn_letter.bind(on_release=self.btn_on_release)
                    self.add_widget(btn_letter)
                    i += 1
        else:
            btn_letter = GridButton(0, 0, text='HOME')
            btn_letter.bind(on_release=self.btn_on_release)
            self.add_widget(btn_letter)
            btn_letter = GridButton(1, 0, text='/')
            btn_letter.bind(on_release=self.btn_on_release)
            self.add_widget(btn_letter)

    def update_grid(self, _instr=None):
        for btn in self.children:
            btn.height = self.row_height
        self.height = len(self.row_values) * self.row_height

    def get_value(self):
        for btn in self.children:
            if btn.state == 'down':
                if btn.text.find(':') >= 0:
                    return btn.text.strip() + '\\'
                elif btn.text.lower().find('home') >= 0:
                    return os.environ['HOME']
                else:
                    return '/'

    def set_value(self, value):
        for btn in self.children:
            if btn.text.strip() == value:
                btn.state = 'down'
                return True

    def btn_on_release(self, widget):
        if self.file_chooser and (widget.state == 'down'):
            self.file_chooser.path = self.get_value()


class GridButton(MyToggleButton):

    def __init__(self, row_index, col_index, **kwargs):
        super().__init__(**kwargs)
        self.row_index = row_index
        self.col_index = col_index
        self.size_hint = (1, None)

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
