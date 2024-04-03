import os

from kivy.graphics import Callback
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListLayout
from kivy.uix.textinput import TextInput

from functions import button_height
from myLayout import MyBoxLayout
from scrollBar import VertScrollBar


class MyFileChooser(FileChooserListLayout):
    VIEWNAME = 'list'
    _ENTRY_TEMPLATE = 'FileListEntry'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = self.ids.scrollview
        self.container = BoxLayout()
        self.children[0].clear_widgets()
        self.container.add_widget(scroll)

        title_box = MyBoxLayout()
        title_box.size_hint = (1, None)
        title_box.height = button_height + 8
        title_box.padding = 4
        self.path_text = TextInput(multiline=False)
        self.path_text.bind(on_text_validate=self.path_text_on_text_validate)
        title_box.add_widget(self.path_text)

        self.children[0].add_widget(title_box)
        self.children[0].add_widget(self.container)

        self.canvas.add(Callback(self.scroll_update))

    def scroll_update(self, _instr):
        scroll = None
        scroll_view = self.ids.scrollview
        for widget in self.container.children:
            if isinstance(widget, VertScrollBar):
                scroll = widget
                break

        if scroll_view.viewport_size[1] > scroll_view.height:
            if not scroll:
                self.container.add_widget(VertScrollBar(scroll_view))
        elif scroll:
            self.container.remove_widget(scroll)

        if not self.path_text.focused:
            self.path_text.text = self.controller.path

    def path_text_on_text_validate(self, _widget):
        if os.path.exists(self.path_text.text):
            self.controller.path = self.path_text.text
