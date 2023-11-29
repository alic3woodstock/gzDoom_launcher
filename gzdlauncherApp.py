import kivy
import functions

kivy.require('1.0.7')

from kivy.app import App
# from kivy.lang.builder import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivyFunctions import rectBtnActive

class FrmGzdlauncher(AnchorLayout):
    def on_kv_post(self, widget):
        pass

    def btnCfg_on_state(self, widget):
        panel = self.ids.panelSettings
        if widget.state == 'down':
            panel.width = 200
        else:
            panel.width = 0
        rectBtnActive(widget)

    def btnManage_on_press(self, widget):
        rectBtnActive(widget)

class GzdLauncher(App):
    def build(self):
        frmGzLauncher = FrmGzdlauncher()
        return frmGzLauncher

    def on_start(self):
        functions.setDataPath()
        self.title = "GZDoom Launcher"
        self.icon = functions.pentagram

if __name__ == '__main__':
    GzdLauncher().run()
