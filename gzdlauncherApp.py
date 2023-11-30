import kivy
import functions
import os

kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.stacklayout import StackLayout
from kivyFunctions import change_color
from gameGrid import GameGrid
from gameDef import GameDef
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanelItem
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle


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

    def btnManage_on_press(self, widget):
        change_color(widget)


class GzdLauncher(App):
    def build(self):
        os.environ['KIVY_DEFAULT_FONT'] = ("[‘FreeMono’, "
                                           "‘fonts/FreeMono.ttf’, "
                                           "‘fonts/FreeMonoOblique.ttf’, "
                                           "‘fonts/FreeMonoBold.ttf’, "
                                           "‘fonts/FreeMonoBoldOblique.ttf’]")
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
        gameGrid.text = 'Games'
        self.gameTabs.add_widget(gameGrid)


if __name__ == '__main__':
    GzdLauncher().run()
