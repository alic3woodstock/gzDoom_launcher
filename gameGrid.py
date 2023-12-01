from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivyFunctions import change_color


class GameButton(ToggleButton):
    def __init__(self, game=None, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.game = game


class GameGrid(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games = []
        self.container = StackLayout()
        self.container.orientation = 'lr-tb'
        self.add_widget(self.container)
        # kivyFunctions.change_color(self, use_alternative_color=True)

    def insertGame(self, game=None):
        gameButton = GameButton(game, text=game.name)
        self.container.add_widget(gameButton)
        gameButton.size_hint = (1, None)
        gameButton.height = 42
        gameButton.bind(state=self.btnCfg_on_state)
        self.background_color = [0, 0, 0, 0]
        change_color(gameButton)

    def btnCfg_on_state(self, widget, state):
        if widget.state == 'down':
            for c in self.container.children:
                if c != widget:
                    c.state = 'normal'

        change_color(widget)

    def on_state(self, widget, state):
        if widget.state == 'normal':
            self.background_color = 'black'
        else:
            self.background_color = [0.5, 0.5, 0.5]
            self.background_color = 'white'
