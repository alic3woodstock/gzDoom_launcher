from kivy.graphics import Callback
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from fileChooserDialog import FileChooserDialog
from fileGrid import FileGrid
from functions import text_color, background_color, button_height
from icon import Icon
from myButton import DropdownMainButton, MyButtonBorder, MyCheckBox
from myDropdown import MyDropdown
from myPopup import MyPopup
from scrollBar import VertScrollBar


def open_file_event(input_value, select_dir, _widget):
    popup = MyPopup()
    popup.content = FileChooserDialog(popup, input_value, select_dir)
    popup.open()


class GenericForm(BoxLayout):
    def __init__(self, height=0, **kwargs):
        super().__init__(**kwargs)
        self.scroll_bar = None

        self.scroll = ScrollView()
        self.scroll.scroll_type = ['bars']
        self.scroll.always_overscroll = False
        self.scroll.bar_width = 4

        self.topLayout = GridLayout()
        self.topLayout.cols = 2
        self.topLayout.padding = [16, 16]
        self.topLayout.spacing = [16, 16]
        self.topLayout.size_hint = (1, None)
        self.topLayout.height = height

        self.values = []
        self.labels = []
        self.children_height = button_height
        self.scroll.add_widget(self.topLayout)
        self.add_widget(self.scroll)
        self.canvas.add(Callback(self.update_form))

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
        self.topLayout.add_widget(label)
        self.topLayout.add_widget(value_input)
        self.ids[field_name] = value_input
        self.ids[field_name + '_l'] = label
        self.ids[field_name + '_b'] = value_input

    def add_checkbox_field(self, text='', field_name=''):
        check_box = MyCheckBox(text=text)
        check_box.height = self.children_height
        check_box.width += self.topLayout.padding[0]
        check_box.id = field_name
        box = BoxLayout(size_hint=(None, None), height=self.children_height)
        self.topLayout.add_widget(box)
        self.topLayout.add_widget(check_box)
        self.ids[field_name] = check_box
        self.ids[field_name + '_l'] = box
        self.ids[field_name + '_b'] = check_box

    def add_checkbox_input(self, text='', field_name=''):
        check_box = MyCheckBox(text=text)
        check_box.height = self.children_height
        field_name1 = field_name + '_check'
        field_name2 = field_name + '_name'
        check_box.id = field_name1
        value_input = TextInput()
        value_input.size_hint = (1, None)
        value_input.height = self.children_height
        value_input.id = field_name2
        self.ids[field_name1] = check_box
        self.ids[field_name2] = value_input
        self.topLayout.add_widget(check_box)
        self.topLayout.add_widget(value_input)
        self.ids[field_name2 + '_l'] = check_box
        self.ids[field_name2 + '_b'] = value_input

    def add_file_field(self, text='', field_name='', select_dir=False):
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
        button_file.fbind('on_release', open_file_event, value_input, select_dir)
        aux_box.add_widget(button_file)

        self.topLayout.add_widget(label)
        box_file.add_widget(value_input)
        box_file.add_widget(aux_box)
        self.topLayout.add_widget(box_file)
        self.ids[field_name] = value_input
        self.ids[field_name + '_l'] = label
        self.ids[field_name + '_b'] = box_file

    def add_dropdown(self, text='', field_name=''):
        label = self.add_label(text)

        main_button = DropdownMainButton()
        main_button.size_hint = (1, 1)
        dropdown = MyDropdown(main_button)

        drop_box = BoxLayout()
        drop_box.size_hint = (1, None)
        drop_box.padding = 2
        drop_box.height = self.children_height
        drop_box.add_widget(main_button)

        self.topLayout.add_widget(label)
        self.topLayout.add_widget(drop_box)
        self.ids[field_name] = dropdown
        self.ids[field_name + '_l'] = label
        self.ids[field_name + '_b'] = drop_box

    def get_value(self, field_name):
        for c in self.topLayoutchildren:
            if isinstance(c, TextInput) and c.id == field_name:
                return c.text

    def get_widget(self, field_name):
        for c in self.topLayout.children:
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

        if self.topLayout.height <= 0:
            self.topLayout.height = (self.get_height() - self.topLayout.padding[1]
                                     - self.topLayout.padding[3])

        scroll = None
        for widget in self.children:
            if isinstance(widget, VertScrollBar):
                scroll = widget
                break

        if self.scroll.viewport_size[1] > self.height:
            if not scroll:
                self.scroll_bar = VertScrollBar(self.scroll)
                self.add_widget(self.scroll_bar)
        elif scroll:
            self.remove_widget(scroll)
            self.scroll_bar = None

    def add_file_list(self, input_widget, field_name=''):
        label = self.add_label('')
        top_grid = FileGrid(input_widget)

        self.topLayout.add_widget(label)
        self.topLayout.add_widget(top_grid)
        self.ids[field_name] = top_grid

    def get_height(self):
        return ((self.children_height + self.topLayout.spacing[1])
                * (len(self.topLayout.children) // self.topLayout.cols)
                + self.topLayout.padding[1] + self.topLayout.padding[3])

    def link_file_list(self, file_list_id, input_id):
        button = self.ids[input_id].parent.children[0].children[0]
        uid = button.get_property_observers(name='on_release', args=True)
        if uid:
            uid = uid[0][4]
            button.unbind_uid('on_release', uid)
        button.fbind('on_release', open_file_event, self.ids[file_list_id], False)

    def hide_field(self, field_name, hide=True, start_index=0):
        if hide:
            self.topLayout.remove_widget(self.ids[field_name + '_l'])
            self.topLayout.remove_widget(self.ids[field_name + '_b'])
        else:
            self.topLayout.add_widget(self.ids[field_name + '_l'], index=start_index)
            self.topLayout.add_widget(self.ids[field_name + '_b'], index=start_index)
