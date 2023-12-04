import kivy
import kivy
import functions
import os

kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Callback
from gameGrid import GameGrid
from gameDef import GameDef
from kivyFunctions import border_color, GetBorders
from gameDefDb import GameDefDb


class FrmGzdlauncher(BoxLayout):
    def main_menu_cb(self, inter):
        main_menu = self.ids.mainMenu
        p = GetBorders(main_menu)
        main_menu.canvas.clear()
        with main_menu.canvas.after:
            Color(border_color)
            Line(points=[p.bottom_left, p.bottom_right])


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
        print('Manage Games 1')


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

        self.ReadDB()

    def ReadDB(self):
        self.gameTabs.clear_tabs()
        gameData = GameDefDb()
        dbTabs = gameData.SelectAllGameTabConfigs()
        games = gameData.SelectAllGames()
        for tab in dbTabs:
            if tab.IsEnabled():
                self.gameTabs.add_tab(tab.GetName(), tab.GetIndex())

        for game in games:
            self.gameTabs.insert_game(game)

        self.gameTabs.select_tab(0)

if __name__ == '__main__':
    GzdLauncher().run()
