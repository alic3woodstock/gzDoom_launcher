from functools import partial
from threading import Thread

import kivy
from kivy.graphics import Callback
from kivy.metrics import Metrics

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
Config.set('graphics', 'custom_titlebar', '1')
Config.set('graphics', 'resizable', '0')
# Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'minimum_width', '640')
Config.set('graphics', 'minimum_height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from frmManageGames import FrmManageGames
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock
from myButton import TopMenuButton
from gameDefDb import GameDefDb
from myPopup import MyPopup, Dialog, Progress
from menu import Menu
from gameFile import GameFile


def run_game(game):
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


class FrmGzdlauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        menuApp = Menu()
        menuApp.bind(on_select=self.menuApp_on_select)
        btnMenuApp = TopMenuButton(menuApp, text='Application')
        self.ids.mainMenu.add_widget(btnMenuApp)

        menuGames = Menu()
        menuGames.bind(on_select=self.menuGames_on_select)
        btnMenuGames = TopMenuButton(menuGames, text='Games')
        self.ids.mainMenu.add_widget(btnMenuGames)

        menuGames.add_item('Manage Games')
        menuGames.add_item('Reset to Default')
        menuGames.add_item('Replace Doom Wad')
        menuGames.add_item('Replace Heretic Wad')

        menuApp.add_item('Update GZDoom')
        menuApp.add_item('Settings')
        menuApp.add_item('About')
        menuApp.add_item('Exit')

        self.menuApp = menuApp
        self.menuGames = menuGames
        self.popup = MyPopup()
        self.height = Window.height - 32
        self.ids.mainMenu.canvas.add(Callback(self.main_menu_cupdate))
        Window.bind(mouse_pos=self.mouse_pos)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        gameTabs = self.ids.gameTabs
        if not self.popup.is_open:
            if keycode[1] == 'left':
                gameTabs.carousel.load_previous()
            elif keycode[1] == 'right':
                gameTabs.carousel.load_next()
            elif keycode[1] == 'down':
                gameTabs.carousel.current_slide.children[0].load_next()
            elif keycode[1] == 'up':
                gameTabs.carousel.current_slide.children[0].load_previous()
            elif keycode[1] == 'pagedown':
                gameTabs.carousel.current_slide.children[0].page_down()
            elif keycode[1] == 'pageup':
                gameTabs.carousel.current_slide.children[0].page_up()
            elif keycode[1] == 'spacebar':
                gameTabs.spacebar()
            elif keycode[1] == 'enter':
                run_game(gameTabs.get_run_params())
        elif isinstance(self.popup.content, FrmManageGames):
            if keycode[1] == 'down':
                self.popup.content.topLayout.load_next()
            elif keycode[1] == 'up':
                self.popup.content.topLayout.load_previous()
            elif keycode[1] == 'pagedown':
                self.popup.content.topLayout.page_down()
            elif keycode[1] == 'pageup':
                self.popup.content.topLayout.page_up()

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            if self.popup.is_open:
                self.popup.dismiss()
            else:
                Window.close()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def btnRun_on_press(self, widget):
        run_game(self.ids.gameTabs.get_run_params())

    def menuGames_on_select(self, widget, data):
        self.popup.title = data.text
        if data.index == 0:
            dialog = FrmManageGames(self.popup)
            self.popup.content = dialog
        elif data.index == 1:
            dialog = Dialog(self.popup,
                            text="This will reset game database to the default values.\n"
                                 + "Do you want to continue?",
                            txtCancel='No', txtOk='Yes', icon='exclamation')
            dialog.btnOk.bind(on_press=self.btnYes1_onPress)
            self.popup.content = dialog
        else:
            self.popup.content = Dialog(self.popup, text='Under contruction', txtCancel='OK', txtOk='',
                                        icon='information')
        self.popup.open()

    def btnYes1_onPress(self, widget):
        progress = Progress(self.popup, text='Starting')
        self.popup.content = progress
        gameFile = GameFile()
        progressClock = Clock.schedule_interval(partial(self.progress_update, progress, gameFile), 0.1)
        gameFile.clock = progressClock
        thread = Thread(target=gameFile.extractAll)
        thread.start()

    def btnUpdate_onPress(self, widget):
        progress = Progress(self.popup, text='Updating GZDoom...')
        self.popup.content = progress
        self.popup.width = 600
        self.popup.height = 200
        gameFile = GameFile()
        progressClock = Clock.schedule_interval(partial(self.progress_update, progress, gameFile), 0.1)
        gameFile.clock = progressClock
        thread = Thread(target=gameFile.verifyUpdate)
        thread.start()

    def progress_update(self, progress, gameFile, *args):
        progress.max = gameFile.max_range
        progress.update_progress(gameFile.value, gameFile.message)
        if gameFile.done:
            self.popup.content = Dialog(self.popup, text=gameFile.message, txtCancel='OK', txtOk='',
                                        icon='information')

    def menuApp_on_select(self, widget, data):
        if data.index == 3:
            Clock.schedule_once(lambda close: Window.close(), 0)
        else:
            self.popup.title = data.text
            if data.index == 0:
                self.btnUpdate_onPress(data)
            elif data.index == 2:
                self.popup.content = Dialog(self.popup, text="GZDoom launcher " + functions.APPVERSION
                                                             + "\nBy Alice Woodtstock 2022-2023",
                                            txtCancel='OK', txtOk='', icon='pentagram')
            else:
                self.popup.content = Dialog(self.popup, text='Under contruction', txtCancel='OK', txtOk='',
                                            icon='information')

            self.popup.open()

    def ReadDB(self):
        gameTabs = self.ids.gameTabs
        gameTabs.clear_tabs()
        gameData = GameDefDb()
        dbTabs = gameData.SelectAllGameTabConfigs()
        games = gameData.SelectAllGames()
        for tab in dbTabs:
            if tab.IsEnabled():
                gameTabs.add_tab(tab.GetName(), tab.GetIndex())

        for game in games:
            gameTabs.insert_game(game)

        for slide in gameTabs.carousel.slides:
            slide.children[0].select_index(0)

        gameTabs.select_tab(0)

    def mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        x = pos[0] * Metrics.dpi / 96
        y = pos[1] * Metrics.dpi / 96
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
                        Clock.schedule_once(btn.on_release, 0)

        for btn in topPanel.children:
            if btn.isDropOpen:
                dropItens = btn.dropdown.container.children[0].children
                for dropItem in dropItens:
                    pos = dropItem.to_widget(x, y)
                    dropItem.hover = dropItem.collide_point(*pos)
                    dropItem.update_button(pos)

    def dummy_function(self, widget, value):
        pass

    def main_menu_cupdate(self, instr):
        i = 0
        for c in self.ids.mainMenu.children:
            i += c.width
        self.ids.mainMenu.width = i + self.ids.mainMenu.padding[2] * 2


class GzdLauncher(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frmGzLauncher = None

    def build(self):
        self.frmGzLauncher = FrmGzdlauncher()
        return self.frmGzLauncher

    def on_start(self):
        functions.setDataPath()
        self.title = "GZDoom Launcher"
        self.icon = functions.pentagram
        Window.set_custom_titlebar(BoxLayout())

        gameDefDb = GameDefDb()

        if not os.path.isfile(functions.dbPath):
            gameDefDb.CreateGameTable()
        else:
            gameDefDb.UpdateDatabase()

        self.frmGzLauncher.ReadDB()


if __name__ == '__main__':
    GzdLauncher().run()
