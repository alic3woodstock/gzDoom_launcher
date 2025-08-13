import os

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser

from dataPath import data_path
from fileGrid import FileGrid
from gridContainer import GridContainer
from localDriveGrid import LocalDriveGrid
from myFileChooser import MyFileChooser
from myPopup import ModalWindow, FileProgress


class FileChooserDialog(ModalWindow):

    def __init__(self, dialog, txt_input, select_dir=False, **kwargs):
        super().__init__(dialog, **kwargs)
        file_grid = BoxLayout()

        file_chooser = FileChooser()
        self.path_grid = LocalDriveGrid(file_chooser)
        self.path_grid.get_values()
        self.path_grid.size_hint = (1, None)
        path_container = GridContainer(grid=self.path_grid)
        path_container.padding = 0
        path_container.size_hint = (None, 1)
        path_container.width = 200
        path_container.container.size_hint = (1, 1)
        file_grid.add_widget(path_container)

        file_chooser.path = data_path().data
        if os.name == 'nt':
            self.path_grid.set_value(data_path().data[:2])
        else:
            home = os.environ['HOME']
            if data_path().data.find(home) >= 0:
                self.path_grid.set_value('HOME')
            else:
                self.path_grid.set_value('/')
        file_chooser.progress_cls = FileProgress
        file_list = MyFileChooser()
        file_chooser.add_widget(file_list)
        self.file_chooser = file_chooser
        file_grid.add_widget(file_chooser)

        self.add_widget(file_grid)
        self.create_box_buttons(txt_ok='OK', txt_cancel=_('Cancel'))
        self.btnOk.bind(on_release=self.on_ok_click)
        self.dialog.height = Window.height
        self.txt_input = txt_input
        self.select_dir = select_dir

    def on_ok_click(self, _widget):
        if self.select_dir:
            if isinstance(self.txt_input, FileGrid):
                self.txt_input.add_value(self.file_chooser.path.strip())
            else:
                self.txt_input.text = self.file_chooser.path.strip()
        elif len(self.file_chooser.selection) > 0:
            if isinstance(self.txt_input, FileGrid):
                self.txt_input.add_value(self.file_chooser.selection[0])
            else:
                self.txt_input.text = self.file_chooser.selection[0]
        self.dialog.dismiss()
