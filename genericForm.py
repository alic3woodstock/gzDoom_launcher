from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from functions import text_color, background_color, button_height
from myButton import MyCheckBox, DropdownItem


class GenericForm(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        self.padding = 16
        self.values = []
        self.labels = []
        self.spacing = 16
        self.children_height = button_height

    def add_label(self, text):
        label = Label()
        label.text = text
        label.background_color = background_color
        label.text_color = text_color
        label.height = self.children_height
        label.size_hint = (None, None)
        label.halign = 'left'
        label.valign = 'middle'
        anchor = AnchorLayout()
        anchor.anchor_x = 'left'
        anchor.anchor_y = 'center'
        anchor.size_hint = (None, None)
        anchor.height = self.children_height
        anchor.add_widget(label)
        self.labels.append(label)
        return anchor

    def add_text_field(self, text='', field_name=''):
        label = self.add_label(text)
        value_input = TextInput()
        value_input.size_hint = (1, None)
        value_input.height = self.children_height
        value_input.id = field_name
        self.add_widget(label)
        self.add_widget(value_input)

    def add_checkbox(self, text='', field_name=''):
        checkBox = MyCheckBox()
        checkBox.size_hint = (None, 1)
        checkBox.width = self.children_height - 16
        label = self.add_label(text)

        container = GridLayout()
        container.cols = 2
        container.padding = 1
        container.spacing = 12
        container.size_hint = (1, None)
        container.height = self.children_height
        container.add_widget(checkBox)
        container.add_widget(label)
        container.id = field_name

        self.add_widget(BoxLayout(size_hint=(None, None), height=self.children_height))
        self.add_widget(container)

        self.canvas.add(Callback(self.update_form))

    def add_dropdown(self, text='', field_name=''):
        label = self.add_label(text)

        mainButton = DropdownItem()
        mainButton.id = field_name
        mainButton.size_hint = (1, 1)

        dropBox = BoxLayout()
        dropBox.size_hint = (1, None)
        dropBox.padding = 2
        dropBox.height = self.children_height
        dropBox.add_widget(mainButton)

        self.add_widget(label)
        self.add_widget(dropBox)


    def get_value(self, field_name):
        for c in self.children:
            if isinstance(c, TextInput) and c.id == field_name:
                return c.text

    def update_form(self, instr):
        max_size = 0
        for lb in self.labels:
            size_x = lb.texture_size[0]
            lb.width = size_x
            if size_x > max_size:
                max_size = size_x

        for lb in self.labels:
            lb.parent.width = max_size
