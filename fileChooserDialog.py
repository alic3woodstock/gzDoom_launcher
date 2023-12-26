from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooser

from myFileChooser import MyFileChooser
from myPopup import ModalWindow, FileProgress


class FileChooserDialog(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        file_grid = BoxLayout()

        file_chooser = FileChooser()
        file_chooser.path = 'D:\\'
        file_chooser.progress_cls = FileProgress
        file_chooser.add_widget(MyFileChooser())
        file_grid.add_widget(file_chooser)

        self.add_widget(file_grid)
        self.CreateBoxButtons(txtOk='OK', txtCancel='Cancel')
        self.dialog.size = Window.size
