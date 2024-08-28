from kivy.uix.gridlayout import GridLayout

from functions import button_height
from gameDef import GameDef
from myButton import MyToggleButton


class GameGrid(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.row_height = button_height

        self.cols = 1
        self.size_hint = (1, None)
        self.height = 0

        self.games = []
        self.empty_game = GameDef(game_id=0, name='Empty Tab', tab_id=-2)
        self.empty_game.exec = ''
        self.insert_game(self.empty_game)
        self.container = None

    def insert_game(self, game=None):
        if self.empty_game and game != self.empty_game:
            self.remove_game(self.empty_game)
            self.empty_game = None

        game_button = GameButton(row_index=len(self.children), game=game, text=game.name)
        self.add_widget(game_button)
        game_button.height = self.row_height
        self.height += game_button.height

    def on_change_selection(self, widget):
        pass  # Used in game carousel to populate mods

    def get_game_btn(self):
        for gameBtn in self.children:
            if gameBtn.state == 'down':
                return gameBtn

    def get_game(self):
        return self.get_game_btn().game

    def remove_game(self, game):
        for btn in self.children:
            if game == btn.game:
                self.remove_widget(btn)
                self.height = self.row_height * len(self.children)


class GameButton(MyToggleButton):
    def __init__(self, row_index=0, game=None, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.size_hint = (1, None)
        self.row_index = row_index

    def on_state(self, widget, value):
        if value == 'down':
            scroll = self.parent.scroll
            if scroll:
                scroll.scroll_to(widget, padding=0)
            for c in self.parent.children:
                if c != widget:
                    c.state = 'normal'
            self.parent.on_change_selection(widget)

    def on_press(self):
        if self.state == 'normal':
            self.state = 'down'
