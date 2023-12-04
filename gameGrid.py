from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from myLayout import MyBoxLayout
from kivyFunctions import change_color


class GameButton(ToggleButton):
    def __init__(self, game=None, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.game = game


class GameGrid(MyBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games = []
        self.lineWidth = 1

        self.scroll = ScrollView()
        self.scroll.bar_width = 4
        self.container = StackLayout()
        self.container.orientation = 'lr-tb'
        self.container.size_hint = (1, None)
        self.container.height = 0
        self.scroll.add_widget(self.container)
        self.add_widget(self.scroll)
        # kivyFunctions.change_color(self, use_alternative_color=True)

    def insert_game(self, game=None):
        gameButton = GameButton(game, text=game.name)
        self.container.add_widget(gameButton)
        gameButton.size_hint = (1, None)
        gameButton.height = 42
        self.container.height += gameButton.height
        gameButton.bind(state=self.btnCfg_on_state)
        gameButton.bind(on_press=self.btnCfg_on_press)
        # self.background_color = [0, 0, 0, 0]
        change_color(gameButton)
        if len(self.container.children) == 1:
            gameButton.state = 'down'

    def btnCfg_on_state(self, widget, state):
        if widget.state == 'down':
            for c in self.container.children:
                if c != widget:
                    c.state = 'normal'

        change_color(widget)

    def btnCfg_on_press(self, widget):
        if widget.state == 'normal':
            widget.state = 'down'


    def on_state(self, widget, state):
        if widget.state == 'normal':
            self.background_color = 'black'
        else:
            self.background_color = [0.5, 0.5, 0.5]
            self.background_color = 'white'

    def get_game(self):
        for gameBtn in self.container.children:
            if gameBtn.state == 'down':
                return gameBtn.game

    def get_index(self):
        if len(self.container.children) > 0:
            for i in range(len(self.container.children)):
                if self.container.children[i].state == 'down':
                    return i

    def select_game_index(self, index):
        if index < len(self.container.children) and index >= 0:
            self.container.children[index].state = 'down'

    def load_next_game(self):
        index = self.get_index()
        if index > 0:
            self.select_game_index(index - 1)

    def load_previous_game(self):
        index = self.get_index()
        if index < (len(self.container.children)):
            self.select_game_index(index + 1)
