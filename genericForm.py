from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from Mydropdown import MyDropdown
from dbGrid import DBGrid
from fileChooserDialog import FileChooserDialog
from functions import text_color, background_color, button_height
from gridContainer import GridContainer
from icon import Icon
from myButton import MyCheckBox, DropdownMainButton, MyButtonBorder
from myPopup import MyPopup


def open_file_dialog(txt_input):
    popup = MyPopup()
    popup.content = FileChooserDialog(popup, txt_input)
    popup.open()


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
        self.ids[field_name] = value_input

    def add_checkbox(self, text='', field_name=''):
        checkBox = MyCheckBox()
        checkBox.size_hint = (None, 1)
        checkBox.width = self.children_height - 16
        checkBox.id = field_name
        label = self.add_label(text)

        container = GridLayout()
        container.cols = 2
        container.padding = 1
        container.spacing = 12
        container.size_hint = (1, None)
        container.height = self.children_height
        container.add_widget(checkBox)
        container.add_widget(label)

        self.add_widget(BoxLayout(size_hint=(None, None), height=self.children_height))
        self.add_widget(container)

        self.canvas.add(Callback(self.update_form))
        self.ids[field_name] = checkBox

    def add_file_field(self, text='', field_name=''):
        label = self.add_label(text)
        value_input = TextInput()
        value_input.id = field_name

        box_file = GridLayout()
        box_file.cols = 2
        box_file.size_hint = (1, None)
        box_file.height = self.children_height

        aux_box = BoxLayout()
        aux_box.padding = 2
        aux_box.size_hint = (None, None)
        aux_box.height = self.children_height
        aux_box.width = self.children_height
        button_file = MyButtonBorder(icon=Icon('folder'))
        button_file.size_hint = (1, 1)
        button_file.bind(on_release=lambda f: open_file_dialog(txt_input=value_input))
        aux_box.add_widget(button_file)

        self.add_widget(label)
        box_file.add_widget(value_input)
        box_file.add_widget(aux_box)
        self.add_widget(box_file)
        self.ids[field_name] = value_input

    def add_dropdown(self, text='', field_name=''):
        label = self.add_label(text)

        mainButton = DropdownMainButton()
        mainButton.size_hint = (1, 1)
        dropdown = MyDropdown(mainButton)

        dropBox = BoxLayout()
        dropBox.size_hint = (1, None)
        dropBox.padding = 2
        dropBox.height = self.children_height
        dropBox.add_widget(mainButton)

        self.add_widget(label)
        self.add_widget(dropBox)
        self.ids[field_name] = dropdown

    def get_value(self, field_name):
        for c in self.children:
            if isinstance(c, TextInput) and c.id == field_name:
                return c.text

    def get_widget(self, field_name):
        for c in self.children:
            if c.id == field_name:
                return c

    def update_form(self, _instr):
        max_size = 0
        for lb in self.labels:
            size_x = lb.texture_size[0]
            lb.width = size_x
            if size_x > max_size:
                max_size = size_x

        for lb in self.labels:
            lb.parent.width = max_size

    def add_file_list(self, text='', field_name=''):
        label = self.add_label(text)
        # label.height = 100
        grid = DBGrid()
        file_grid = GridContainer(grid=grid, has_title=False)
        file_grid.container.size_hint = (1, 1)
        grid.size_hint = (1, None)
        file_grid.padding = 2

        top_grid = BoxLayout()
        top_grid.orientation = 'horizontal'
        top_grid.add_widget(file_grid)

        box_buttons = GridLayout(rows=3, cols=1, size_hint=(None, 1), width=108,
                                 padding=[6, 2, 2, 2])

        action_buttons = [MyButtonBorder(text="Add"), MyButtonBorder(text="Del"),
                          MyButtonBorder(text="Clear")]
        for b in action_buttons:
            b.size_hint = (None, None)
            b.width = 100
            b.height = 30
            box_buttons.add_widget(b)

        top_grid.add_widget(box_buttons)

        self.add_widget(label)
        self.add_widget(top_grid)
        self.ids[field_name] = grid

    def refresh_file_list(self, index):
        params = [index]
        grid = self.ids.filelist
        if grid:
            grid.get_values(['id', 'Filename'],
                            """SELECT id,file FROM FILES WHERE gameid=?""", params)
