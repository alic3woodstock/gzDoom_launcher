from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown


class MyDropdown(DropDown):

    def __init__(self, main_button, **kwargs):
        super().__init__(**kwargs)
        self.main_button = main_button
        self.main_button.bind(on_release=self.open)

    def on_select(self, data):
        self.main_button.text = data.name
        self.main_button.game = data
        self.main_button.state = 'normal'

    def on_dismiss(self):
        self.main_button.state = 'normal'

    def create_dropbox(self):
        self.main_button.size_hint = (1, 1)
        drop_box = BoxLayout()
        drop_box.size_hint = (1, None)
        drop_box.padding = 2
        drop_box.add_widget(self.main_button)
        return drop_box

