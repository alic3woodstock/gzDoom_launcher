from functools import partial
from threading import Thread

import kivy
import functions
import subprocess
import os

from kivy.config import Config
kivy.require('2.1.0')
Config.set('kivy', 'default_font', '["RobotoMono", '
                                   '"fonts/RobotoMono-Regular.ttf", '
                                   '"fonts/RobotoMono-Italic.ttf", '
                                   '"fonts/RobotoMono-Bold.ttf", '
                                   '"fonts/RobotoMono-BoldItalic.ttf"]')

Config.set('kivy', 'kivy_clock', 'free_all')
Config.set('graphics', 'minimum_width', '640')
Config.set('graphics', 'minimum_height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from myButton import topMenuButton
from gameDefDb import GameDefDb
from myPopup import MyPopup, Dialog, Progress
from menu import Menu
from gameFile import GameFile

class FrmGzdlauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        menuApp = Menu()
        menuApp.bind(on_select=self.menuApp_on_select)
        btnMenuApp = topMenuButton(menuApp, text='Application')
        self.ids.mainMenu.add_widget(btnMenuApp)

        menuGames = Menu()
        menuGames.bind(on_select=self.menuGames_on_select)
        btnMenuGames = topMenuButton(menuGames, text='Games')
        self.ids.mainMenu.add_widget(btnMenuGames)

        menuGames.add_item('Manage Games')
        menuGames.add_item('Reset to Default')
        menuGames.add_item('Replace Doom Wad')
        menuGames.add_item('Replace Heretic Wad')

        menuApp.add_item('Update GZDoom')
        menuApp.add_item('About')
        menuApp.add_item('Exit')

        self.menuApp = menuApp
        self.menuGames = menuGames
        self.popup = MyPopup()
        Window.bind(mouse_pos=self.mouse_pos)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        gameTabs = self.ids.gameTabs
        if keycode[1] == 'left':
            gameTabs.carousel.load_previous()
        elif keycode[1] == 'right':
            gameTabs.carousel.load_next()
        elif keycode[1] == 'down':
            gameTabs.carousel.current_slide.children[0].load_next_game()
        elif keycode[1] == 'up':
            gameTabs.carousel.current_slide.children[0].load_previous_game()
        elif keycode[1] == 'pagedown':
            gameTabs.carousel.current_slide.children[0].page_down()
        elif keycode[1] == 'pageup':
            gameTabs.carousel.current_slide.children[0].page_up()
        elif keycode[1] == 'spacebar':
            gameTabs.spacebar()
        elif keycode[1] == 'enter':
            self.run_game(gameTabs.get_run_params())

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            exit()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def btnRun_on_press(self, widget):
        self.run_game(self.ids.gameTabs.get_run_params())

    def run_game(self, game):
        if game[0]:
            command = []
            if game[0].exec.strip() != "":
                command.append(game[0].exec)

                if game[0].iWad.strip() != "":
                    command.append('-iwad')
                    command.append(game[0].iWad.strip())

                for file in game[0].files:
                    command.append('-file')
                    command.append(file.strip())

                if game[1]:
                    for file in game[1].files:
                        command.append('-file')
                        command.append(file.strip())

                for cmd in list(game[0].cmdParams):
                    command.append(cmd)

                if len(command) > 0:
                    result = subprocess.run(command, shell=True)
                    if result.returncode == 0:
                        gameDefDb = GameDefDb()
                        gameDefDb.UpdateLastRunMod(game[0], game[1])
                        game[0].lastMod = game[1].id
    def menuGames_on_select(self, widget, data):
        self.popup.title = data.text
        if data.index == 1:
            dialog = Dialog(self.popup,
                            text="This will reset game database to the default values.\n"
                                 + "Do you want to continue?",
                            txtCancel='No', txtOk='Yes', icon='exclamation')
            dialog.btnOk.bind(on_press=self.btnYes1_onPress)
            self.popup.content = dialog
        self.popup.open()

    def btnYes1_onPress(self, widget):
        progress = Progress(self.popup, text='Starting')
        self.popup.content = progress
        gameFile = GameFile()
        progressClock = Clock.schedule_interval(partial(self.progress_update, progress, gameFile), 0.1)
        gameFile.clock = progressClock
        thread = Thread(target=gameFile.extractAll)
        thread.start()

    def progress_update(self, progress, gameFile, *args):
        progress.progress.max = gameFile.max_range
        progress.update_progress(gameFile.value, gameFile.message)
        if gameFile.done:
            self.popup.content = Dialog(self.popup, text=gameFile.message, txtCancel='OK', txtOk='',
                                        icon='information')

    def menuApp_on_select(self, widget, data):
        if data.index == 2:
            exit()
        self.popup.title = data.text
        self.popup.open()

    def ReadDB(self):
        gameTabs = self.ids.gameTabs
        gameTabs.clear_tabs()
        gameData = GameDefDb()
        dbTabs = gameData.SelectAllGameTabConfigs()
        games = gameData.SelectAllGames(desc=True)
        for tab in dbTabs:
            if tab.IsEnabled():
                gameTabs.add_tab(tab.GetName(), tab.GetIndex())

        for game in games:
            gameTabs.insert_game(game)

        gameTabs.select_tab(0)

    def mouse_pos(self, *args):
        if not self.get_root_window():
            return  # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        x = pos[0] * Window.dpi / 96
        y = pos[1] * Window.dpi / 96
        topPanel = self.ids.mainMenu
        pressed = False
        btnPressed = None
        for btn in topPanel.children:
            if btn.state == 'down':
                pressed = True
                btnPressed = btn
        if pressed and topPanel.collide_point(x, y):
            for btn in topPanel.children:
                if btn.x <= x <= (btn.x + btn.width):
                    if btn.state == 'normal':
                        btn.state = 'down'
                        btnPressed.dropdown.dismiss()
                        btn.on_state = self.dummy_function
                        Clock.schedule_once(btn.on_release, 0)
    def dummy_function(self, widget, value):
        pass

class GzdLauncher(App):
    def build(self):
        self.frmGzLauncher = FrmGzdlauncher()
        # Window.minimum_width = 640
        # Window.minimum_height = 480
        return self.frmGzLauncher

    def on_start(self):
        functions.setDataPath()
        self.title = "GZDoom Launcher"
        self.icon = functions.pentagram

        gameDefDb = GameDefDb()

        if not os.path.isfile(functions.dbPath):
            gameDefDb.CreateGameTable()
        else:
            gameDefDb.UpdateDatabase()

        self.frmGzLauncher.ReadDB()


if __name__ == '__main__':
    GzdLauncher().run()
