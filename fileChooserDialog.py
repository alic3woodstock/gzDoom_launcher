import os
import string

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser
import functions
from gridContainer import GridContainer
from localDriveGrid import LocalDriveGrid
from myFileChooser import MyFileChooser
from myPopup import ModalWindow, FileProgress


class FileChooserDialog(ModalWindow):

    def __init__(self, dialog, **kwargs):
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

        file_chooser.path = functions.dataPath
        if os.name == 'nt':
            self.path_grid.set_value(functions.dataPath[:2])
        else:
            home = os.environ['HOME']
            if functions.dataPath.find(home) >= 0:
                self.path_grid.set_value('HOME')
            else:
                self.path_grid.set_value('/')
        file_chooser.progress_cls = FileProgress
        file_chooser.add_widget(MyFileChooser())
        file_grid.add_widget(file_chooser)

        self.add_widget(file_grid)
        self.CreateBoxButtons(txtOk='OK', txtCancel='Cancel')
        self.dialog.size = Window.size

