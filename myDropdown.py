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

