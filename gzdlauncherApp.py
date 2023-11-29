import kivy
import functions

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanelItem
from kivy.uix.button import Button

from kivyFunctions import rectBtnActive
from kivy.graphics import Color, Rectangle
from gameGrid import GameGrid
from gameDef import GameDef

class FrmGzdlauncher(StackLayout):
    def on_kv_post(self, widget):
        pass
    def btnCfg_on_state(self, widget):
        panel = self.ids.panelSettings
        if widget.state == 'down':
            panel.width = 200
            self.ids.btnManage.text = 'Manage Games'
            self.ids.btnReset.text = 'Reset to default games'
        else:
            panel.width = 0
            self.ids.btnManage.text = ''
            self.ids.btnReset.text = ''
        rectBtnActive(widget)

    def btnManage_on_press(self, widget):
        rectBtnActive(widget)

class GzdLauncher(App):
    def build(self):
        frmGzLauncher = FrmGzdlauncher()
        self.gameTabs = frmGzLauncher.ids.gameTabs
        return frmGzLauncher

    def on_start(self):
        functions.setDataPath()
        self.title = "GZDoom Launcher"
        self.icon = functions.pentagram

        gameGrid = GameGrid()
        gameGrid.insertGame(GameDef(0, 1, 'Teste Game 1', 0))
        gameGrid.insertGame(GameDef(1, 2, 'Teste Game 2', 0))
        gameGrid.test = 'Games'
        self.gameTabs.add_widget(gameGrid)





if __name__ == '__main__':
    GzdLauncher().run()
