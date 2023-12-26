from kivy.uix.filechooser import FileChooserListLayout

from myPopup import Progress


class MyFileChooser(FileChooserListLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.children[0].children[0].children[0].children)
