from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from myButton import MyToggleButton, button_height
from gameDef import GameDef
from gridContainer import GridContainer


class GameButton(MyToggleButton):
    def __init__(self, game=None, **kwargs):
        super(MyToggleButton, self).__init__(**kwargs)
        self.game = game
        self.size_hint = (1, None)


class GameGrid(GridContainer):
    def __init__(self, **kwargs):
        super().__init__(GridLayout(), **kwargs)
        # self.grid.orientation = 'bt-lr'
        self.grid.cols = 1
        self.grid.size_hint = (1, None)
        self.grid.height = 0

        self.container.size_hint = (1, 1)
        self.row_height = button_height

        self.games = []
        self.empty_game = GameDef(id=0, name='Empty Tab', tab=-2)
        self.empty_game.exec = ''
        self.insert_game(self.empty_game)

    def insert_game(self, game=None):
        if self.empty_game and game != self.empty_game:
            self.remove_game(self.empty_game)
            self.empty_game = None
        gameButton = GameButton(game, text=game.name)
        self.grid.add_widget(gameButton)
        gameButton.height = button_height
        self.grid.height += gameButton.height
        gameButton.bind(state=self.btnCfg_on_state)
        gameButton.bind(on_press=self.btnCfg_on_press)
        # gameButton.state = 'down'

    def btnCfg_on_state(self, widget, state):
        if state == 'down':
            if self.grid.height > self.height:
                self.scroll.scroll_to(widget, padding=0)
            for c in self.grid.children:
                if c != widget:
                    c.state = 'normal'
            self.on_change_selection(widget)


    def btnCfg_on_press(self, widget):
        if widget.state == 'normal':
            widget.state = 'down'

    def on_change_selection(self, widget):
        pass


    def get_game_btn(self):
        for gameBtn in self.grid.children:
            if gameBtn.state == 'down':
                return gameBtn

    def get_game(self):
        return self.get_game_btn().game

    def remove_game(self, game):
        for btn in self.grid.children:
            if game == btn.game:
                self.grid.remove_widget(btn)
                self.grid.height = button_height * len(self.grid.children)

    # def scroll_update(self, instr):
    #     scroll = None
    #     for widget in self.children:
    #         if isinstance(widget, VertScrollBar):
    #             scroll = widget
    #             break
    #
    #     if self.scroll.viewport_size[1] > self.scroll.height:
    #         if not scroll:
    #             self.add_widget(VertScrollBar(self.scroll))
    #     elif scroll:
    #         self.remove_widget(scroll)