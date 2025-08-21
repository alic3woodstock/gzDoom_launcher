import os
import kivy

from configDB import read_config, write_config

os.environ['KIVY_METRICS_DENSITY'] = '1'

kivy.require('2.3.0')
from kivy.config import Config

Config.set('kivy', 'default_font', '["RobotoMono", '
                                   '"fonts/RobotoMono-Regular.ttf", '
                                   '"fonts/RobotoMono-Italic.ttf", '
                                   '"fonts/RobotoMono-Bold.ttf", '
                                   '"fonts/RobotoMono-BoldItalic.ttf"]')

Config.set('kivy', 'kivy_clock', 'free_all')
Config.set('kivy', 'desktop', '1')
Config.set('graphics', 'resizable', '1')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '768')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

import functions
import subprocess
from functions import set_language
from frmCredits import FrmCredits
from frmHelpControls import FrmHelpControls
from frmImportDoom import FrmImportDoom
from gzdoomUpdate import GZDoomUpdate
from screeninfo import get_monitors
from kivy.metrics import Metrics
from functools import partial
from threading import Thread
from gameDefDB import select_all_games, update_last_run_mod
from gameTabDB import select_all_game_tabs
from frmSettings import FrmSettings
from kivy.graphics import Callback
from gameCarousel import GameCarousel
from myLayout import MyStackLayout, MyBoxLayout
from frmManageGames import FrmManageGames
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.core.window import Window
from kivy.clock import Clock
from myButton import TopMenuButton, MyButtonBorder
from createDB import create_game_table, update_database
from myPopup import MyPopup, Dialog, Progress, EmptyDialog
from menu import Menu
from gameFileFunctions import GameFileFunctions
from frmReplaceWad import FrmReplaceWad
from dataPath import DataPath, data_path
from locale import getlocale


class FrmGzdlauncher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        DataPath()

        if not os.path.isfile(data_path().db):
            language = getlocale()[0]
            set_language(language)
            create_game_table()
            write_config("firstrun", True, "bool")
            write_config("language", language, "text")
        else:
            language = read_config("language","text")
            set_language(language)

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
        if language == 'pt_BR':
            run_button.width = 164
        else:
            run_button.width = 128
        run_button.text = _('Run Game')
        run_button.bind(on_release=self.btn_run_on_press)

        box_buttons.add_widget(run_button)
        self.add_widget(box_buttons)

        self.is_game_running = False
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        menu_app = Menu()
        menu_app.bind(on_select=self.menu_app_on_select)
        btn_menu_app = TopMenuButton(menu_app, text=_('Application'))
        self.main_menu.add_widget(btn_menu_app)

        menu_games = Menu()
        menu_games.bind(on_select=self.menu_games_on_select)
        btn_menu_games = TopMenuButton(menu_games, text=_('Games'))
        self.main_menu.add_widget(btn_menu_games)

        menu_help = Menu()
        menu_help.bind(on_select=self.menu_help_on_select)
        btm_menu_help = TopMenuButton(menu_help, text=_('Help'))
        self.main_menu.add_widget(btm_menu_help)

        menu_games.add_item(_('Manage Games'))
        menu_games.add_item(_('Reset to Default'))
        menu_games.add_item(_('Import Doom + Doom II 2024'))
        menu_games.add_item(_('Replace freedoom2.wad'))
        menu_games.add_item(_('Replace blasphemer.wad'))

        menu_app.add_item(_('Update GZDoom'))
        menu_app.add_item(_('Settings'))
        menu_app.add_item(_('Exit'))

        menu_help.add_item(_('Controls'))
        menu_help.add_item(_('Credits'))
        menu_help.add_item(_('About'))

        self.menuApp = menu_app
        self.menuGames = menu_games
        self.menuHelp = menu_help
        self.popup = MyPopup()
        self.popup.bind(on_dismiss=lambda r: self.read_db())
        self.height = Window.height - 32
        self.main_menu.canvas.add(Callback(self.main_menu_cupdate))
        Window.bind(mouse_pos=self.mouse_pos)

    def _keyboard_closed(self):
        pass

    def _on_keyboard_down(self, _keyboard, keycode, _text, _modifiers):
        game_tabs = self.ids.gameTabs
        if not self.popup.is_open and not self.is_game_running:
            if keycode[1] == 'left':
                game_tabs.carousel.load_previous()
            elif keycode[1] == 'right':
                game_tabs.carousel.load_next()
            elif keycode[1] == 'down':
                game_tabs.carousel.current_slide.children[0].load_next()
            elif keycode[1] == 'up':
                game_tabs.carousel.current_slide.children[0].load_previous()
            elif keycode[1] == 'pagedown':
                game_tabs.carousel.current_slide.children[0].page_down()
            elif keycode[1] == 'pageup':
                game_tabs.carousel.current_slide.children[0].page_up()
            elif keycode[1] == 'spacebar':
                game_tabs.spacebar()
            elif keycode[1] == 'enter':
                self.btn_run_on_press(None)
            elif keycode[1] == 'f11':
                if Window.fullscreen != 'auto':
                    Window.fullscreen = 'auto'
                else:
                    Window.fullscreen = 0

        elif isinstance(self.popup.content, FrmManageGames):
            if keycode[1] == 'down':
                self.popup.content.topGrid.load_next()
            elif keycode[1] == 'up':
                self.popup.content.topGrid.load_previous()
            elif keycode[1] == 'pagedown':
                self.popup.content.topGrid.page_down()
            elif keycode[1] == 'pageup':
                self.popup.content.topGrid.page_up()

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

    def btn_run_on_press(self, _widget):
        self.popup.content = EmptyDialog(self.popup, _('Loading...'))
        self.popup.title = ''
        self.popup.open()
        Clock.schedule_once(self.run_game, 1)

    def menu_games_on_select(self, _widget, data):
        self.popup.title = data.text
        if data.index == 0:
            dialog = FrmManageGames(self.popup)
            self.popup.content = dialog
        elif data.index == 1:
            dialog = Dialog(self.popup,
                            text=_("This will reset game database to the default values.\n"
                                   + "Do you want to continue?"),
                            txt_cancel=_('No'), txt_ok=_('Yes'), icon='exclamation')
            dialog.btnOk.bind(on_release=self.btn_yes1_on_press)
            self.popup.content = dialog
        elif data.index == 2:
            self.popup.content = FrmImportDoom(self.popup)
        elif data.index == 3:
            self.popup.content = FrmReplaceWad(self.popup, mod_group=1)
        elif data.index == 4:
            self.popup.content = FrmReplaceWad(self.popup, mod_group=2)
        else:
            self.popup.content = Dialog(self.popup, text=_('Under construction'), txt_cancel=_('OK'), txt_ok='',
                                        icon='information')
        self.popup.open()

    def menu_help_on_select(self, _widget, data):
        self.popup.title = data.text
        if data.index == 0:
            self.popup.content = FrmHelpControls(self.popup)
        elif data.index == 1:
            self.popup.content = FrmCredits(self.popup)
        elif data.index == 2:
            self.popup.content = Dialog(self.popup, text="GZDoom launcher " + functions.APPVERSION
                                                         + "\n" + _('Copyright') + ' © 2022-2025 ' + 'Alice "alic3woodstock" Xavier',
                                        txt_cancel='OK', txt_ok='', icon='pentagram')
        else:
            self.popup.content = Dialog(self.popup, text=_('Under construction'), txt_cancel='OK', txt_ok='',
                                        icon='information')
        self.popup.open()

    def btn_yes1_on_press(self, _widget):
        progress = Progress(self.popup, text=_('Starting'))
        self.popup.content = progress
        game_file = GameFileFunctions()
        progress_clock = Clock.schedule_interval(partial(self.progress_update, progress, game_file), 0.1)
        game_file.clock = progress_clock
        thread = Thread(target=game_file.extract_all)
        thread.start()

    def btn_update_on_press(self, gzdoom_update):
        progress = Progress(self.popup, text=_('Updating GZDoom...'))
        self.popup.content = progress
        self.popup.width = 600
        self.popup.height = 200
        game_file = GameFileFunctions()
        progress_clock = Clock.schedule_interval(partial(self.progress_update, progress, game_file), 0.1)
        game_file.clock = progress_clock
        if isinstance(gzdoom_update, GZDoomUpdate):
            thread = Thread(target=lambda: game_file.update_gz_doom(gzdoom_update))
            thread.start()
        else:
            thread = Thread(target=game_file.verify_update)
            thread.start()

    def progress_update(self, progress, game_file, *_args):
        progress.max = game_file.max_range
        progress.update_progress(game_file.value, game_file.message)
        if game_file.done:
            self.popup.content = Dialog(self.popup, text=game_file.message, txt_cancel=_('OK'), txt_ok='',
                                        icon='information')

    def menu_app_on_select(self, _widget, data):
        if data.index == 3:
            Clock.schedule_once(lambda close: Window.close(), 0)
        else:
            self.popup.title = data.text
            if data.index == 0:
                self.btn_update_on_press(data)
            elif data.index == 1:
                self.popup.content = FrmSettings(self.popup)
            elif data.index == 2:
                Window.close()
            else:
                self.popup.content = Dialog(self.popup, text=_('Under contruction'), txt_cancel='OK', txt_ok='',
                                            icon='information')

            self.popup.open()

    def read_db(self):
        if not self.is_game_running:
            game_tabs = self.ids.gameTabs
            game_tabs.clear_tabs()
            db_tabs = select_all_game_tabs()
            games = select_all_games()
            for tab in db_tabs:
                if tab.is_enabled:
                    game_tabs.add_tab(tab.name, tab.index)

            for game in games:
                game_tabs.insert_game(game)

            for slide in game_tabs.carousel.slides:
                slide.children[0].select_index(0)

            game_tabs.select_tab(0)

    def mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        x = pos[0] * Metrics.dpi / 96
        y = pos[1] * Metrics.dpi / 96
        top_panel = self.main_menu
        pressed = False
        for btn in top_panel.children:
            if btn.state == 'down':
                pressed = True

        if pressed and top_panel.collide_point(x, y):
            for btn in top_panel.children:
                if btn.x < x < (btn.x + btn.width):
                    if btn.state == 'normal':
                        btn.state = 'down'
                        Clock.schedule_once(btn.on_release, 0)
                        for btn2 in top_panel.children:
                            if btn2 != btn:
                                btn2.dropdown.dismiss()
                        break

        for btn in top_panel.children:
            if btn.isDropOpen:
                drop_itens = btn.dropdown.container.children[0].children
                for dropItem in drop_itens:
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

    def run_game(self, _clock=None):
        self.is_game_running = True
        game = self.ids.gameTabs.get_run_params()
        if game[0]:
            command = []
            if game[0].exec.strip() != "":
                if game[0].exec.lower().find('.exe') >= 0 and os.name != "nt":
                    os.environ['WINEPREFIX'] = data_path().data + '/.wine'
                    command.append(data_path().wine)
                command.append(game[0].exec)

                if game[0].iWad.strip() != "":
                    command.append('-iwad')
                    command.append(game[0].iWad.strip())

                if len(game[0].files) > 0:
                    command.append('-file')

                for file in game[0].files:
                    command.append(file.strip())

                if game[1]:
                    if len(game[0].files) <= 0 < len(game[1].files):
                        command.append('-file')
                    for file in game[1].files:
                        command.append(file.strip())

                for cmd in list(game[0].cmdParams):
                    command.append(cmd)

                if ' '.join(command).strip().lower().find('-savedir') < 0:
                    command.append('-savedir')
                    if os.name == 'nt':
                        command.append(data_path().data + '\\saves\\' + str(game[0].id))
                    else:
                        command.append(data_path().data + '/saves/' + str(game[0].id))

                if len(command) > 0:
                    functions.log(command, False)
                    result = subprocess.run(command)
                    if result.returncode == 0:
                        update_last_run_mod(game[0], game[1].id)
                        game[0].lastMod = game[1].id
                        self.ids.gameTabs.update_current_game(game[0])

        self.popup.dismiss()
        self.is_game_running = False

    def check_gzdoom_update(self, _clock=None):
        gzdoom_update = GZDoomUpdate()
        if gzdoom_update.check_gzdoom_update():
            dialog = Dialog(self.popup, _("A new version of GZDoom was found, update now?"),
                            txt_ok=_('Yes'), txt_cancel=_('No'), icon='question')
            self.popup.content = dialog
            dialog.btnOk.bind(on_release=lambda f: self.btn_update_on_press(gzdoom_update))
        else:
            self.popup.dismiss()


class GzdLauncher(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frmGzLauncher = None

    def build(self):
        self.frmGzLauncher = FrmGzdlauncher()
        return self.frmGzLauncher

    def on_start(self):
        monitors = get_monitors()
        m_height = 4096
        for m in monitors:
            if m.is_primary:
                m_height = m.height

        if Metrics.dpi > 120 and m_height <= 1080:  # fix for 1080p and 150% zoom on windows
            Window.fullscreen = 'auto'

        os.chdir(data_path().data)
        self.title = "GZDoom Launcher"
        self.icon = data_path().pentagram

        if read_config("firstrun", "bool"):
            write_config("firstrun", False, "bool")
            dialog = Dialog(self.frmGzLauncher.popup,
                            text=_("Download default games now? (games -> reset to default)"),
                            txt_cancel=_('No'), txt_ok=_('Yes'), icon='exclamation')
            dialog.btnOk.bind(on_release=self.frmGzLauncher.btn_yes1_on_press)
            self.frmGzLauncher.popup.content = dialog
            self.frmGzLauncher.popup.open()
        else:
            update_database()
            if read_config('checkupdate', 'bool'):
                popup = self.frmGzLauncher.popup
                popup.content = EmptyDialog(popup,
                                            _('Checking GZDoom version...'))
                popup.open()
                Clock.schedule_once(callback=self.frmGzLauncher.check_gzdoom_update, timeout=1)
            self.frmGzLauncher.read_db()


if __name__ == '__main__':
    GzdLauncher().run()
