import os
import subprocess
from functools import partial
from threading import Thread

import kivy
from kivy.config import Config
from kivy.graphics import Callback
from kivy.metrics import Metrics

import functions
from gameCarousel import GameCarousel
from myLayout import MyStackLayout, MyBoxLayout

kivy.require('2.1.0')
Config.set('kivy', 'default_font', '["RobotoMono", '
                                   '"fonts/RobotoMono-Regular.ttf", '
                                   '"fonts/RobotoMono-Italic.ttf", '
                                   '"fonts/RobotoMono-Bold.ttf", '
                                   '"fonts/RobotoMono-BoldItalic.ttf"]')

Config.set('kivy', 'kivy_clock', 'free_all')
Config.set('graphics', 'borderless', '0')
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'minimum_width', '640')
Config.set('graphics', 'minimum_height', '480')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from frmManageGames import FrmManageGames
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivy.clock import Clock
from myButton import TopMenuButton, MyButtonBorder
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
                print(command)
                result = subprocess.run(command, shell=True)
                if result.returncode == 0:
                    gameDefDb = GameDefDb()
                    gameDefDb.UpdateLastRunMod(game[0], game[1])
                    game[0].lastMod = game[1].id


class FrmGzdlauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 1

        main_menu_box = BoxLayout()
        main_menu_box.size_hint = (1, None)
        main_menu_box.height = 42

        self.main_menu = StackLayout()
        self.main_menu.padding = (0, 0, 2, 4)
        self.main_menu.size_hint = (None, 1)

        main_menu_box.add_widget(self.main_menu)
        self.add_widget(main_menu_box)

        main_box = BoxLayout()
        main_box.id = 'mainBox'
        main_box.orientation = 'horizontal'

        game_panel = MyBoxLayout()
        game_panel.id = 'gamePanel'
        game_panel.orientation = 'vertical'
        game_panel.borders = ['left', 'right', 'bottom']

        game_carousel = GameCarousel()
        game_carousel.id = 'gameTabs'
        game_carousel.do_default_tab = False

        self.ids['mainBox'] = main_box
        self.ids['gamePanel'] = game_panel
        self.ids['gameTabs'] = game_carousel

        game_panel.add_widget(game_carousel)
        main_box.add_widget(game_panel)
        self.add_widget(main_box)

        box_buttons = MyStackLayout()
        box_buttons.size_hint = (1, None)
        box_buttons.height = 64
        box_buttons.orientation = 'rl-tb'
        box_buttons.padding = (8, 10, 8, 8)
        box_buttons.borders = ['left', 'right', 'bottom']

        run_button = MyButtonBorder()
        run_button.size_hint = (None, 1)
        run_button.width = 128
        run_button.text = 'Run Game'
        run_button.bind(on_release=self.btnRun_on_press)

        box_buttons.add_widget(run_button)
        self.add_widget(box_buttons)


        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        menuApp = Menu()
        menuApp.bind(on_select=self.menuApp_on_select)
        btnMenuApp = TopMenuButton(menuApp, text='Application')
        self.main_menu.add_widget(btnMenuApp)

        menuGames = Menu()
        menuGames.bind(on_select=self.menuGames_on_select)
        btnMenuGames = TopMenuButton(menuGames, text='Games')
        self.main_menu.add_widget(btnMenuGames)

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
        self.main_menu.canvas.add(Callback(self.main_menu_cupdate))
        Window.bind(mouse_pos=self.mouse_pos)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, _keyboard, keycode, _text, _modifiers):
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
                self.popup.content.topGrid.load_next()
            elif keycode[1] == 'up':
                self.popup.content.topGrid.load_previous()
            elif keycode[1] == 'pagedown':
                self.popup.content.topGrid.page_down()
            elif keycode[1] == 'pageup':
                self.popup.content.topGrid.page_up()

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            if (isinstance(self.popup.content, FrmManageGames)
                    and self.popup.content.popup
                    and self.popup.content.popup.is_open):
                self.popup.content.popup.dismiss()
            elif self.popup.is_open:
                self.popup.dismiss()
            else:
                Window.close()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def btnRun_on_press(self, _widget):
        run_game(self.ids.gameTabs.get_run_params())

    def menuGames_on_select(self, _widget, data):
        self.popup.title = data.text
        if data.index == 0:
            dialog = FrmManageGames(self.popup)
            self.popup.content = dialog
        elif data.index == 1:
            dialog = Dialog(self.popup,
                            text="This will reset game database to the default values.\n"
                                 + "Do you want to continue?",
                            txtCancel='No', txtOk='Yes', icon='exclamation')
            dialog.btnOk.bind(on_release=self.btnYes1_onPress)
            self.popup.content = dialog
        else:
            self.popup.content = Dialog(self.popup, text='Under contruction', txtCancel='OK', txtOk='',
                                        icon='information')
        self.popup.open()

    def btnYes1_onPress(self, _widget):
        progress = Progress(self.popup, text='Starting')
        self.popup.content = progress
        gameFile = GameFile()
        progressClock = Clock.schedule_interval(partial(self.progress_update, progress, gameFile), 0.1)
        gameFile.clock = progressClock
        thread = Thread(target=gameFile.extractAll)
        thread.start()

    def btnUpdate_onPress(self, _widget):
        progress = Progress(self.popup, text='Updating GZDoom...')
        self.popup.content = progress
        self.popup.width = 600
        self.popup.height = 200
        gameFile = GameFile()
        progressClock = Clock.schedule_interval(partial(self.progress_update, progress, gameFile), 0.1)
        gameFile.clock = progressClock
        thread = Thread(target=gameFile.verifyUpdate)
        thread.start()

    def progress_update(self, progress, gameFile, *_args):
        progress.max = gameFile.max_range
        progress.update_progress(gameFile.value, gameFile.message)
        if gameFile.done:
            self.popup.content = Dialog(self.popup, text=gameFile.message, txtCancel='OK', txtOk='',
                                        icon='information')

    def menuApp_on_select(self, _widget, data):
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
        topPanel = self.main_menu
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

    def main_menu_cupdate(self, _instr):
        i = 0
        for c in self.main_menu.children:
            i += c.width
        self.main_menu.width = i + self.main_menu.padding[2] * 2


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

        gameDefDb = GameDefDb()

        if not os.path.isfile(functions.dbPath):
            gameDefDb.CreateGameTable()
        else:
            gameDefDb.UpdateDatabase()

        self.frmGzLauncher.ReadDB()


if __name__ == '__main__':
    GzdLauncher().run()
