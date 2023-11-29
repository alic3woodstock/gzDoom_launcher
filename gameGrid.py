from kivy.graphics import Color, Rectangle
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivyFunctions import rectBtnActive

class GameButton(ToggleButton):
    def __init__(self, game = None, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.game = game

class GameGrid(TabbedPanelItem):
    def __init__(self, **kwargs):
        super(TabbedPanelItem, self).__init__(**kwargs)
        self.orientation = 'lr-tb'
        self.games = []
        self.container = StackLayout()
        self.container.orientation = 'lr-tb'
        self.add_widget(self.container)
        # with self.canvas:
        #     Color('white')
        #     Rectangle(pos=self.pos, size=self.size)


    def insertGame(self, game = None):
        gameButton = GameButton(game, text=game.name)
        self.container.add_widget(gameButton)
        gameButton.size_hint = (1, None)
        gameButton.height = 42
        gameButton.bind(state=self.btnCfg_on_state)
        rectBtnActive(gameButton)
    def btnCfg_on_state(self, widget, state):
        if widget.state == 'down':
            for c in self.content.children:
                if c != widget:
                    c.state = 'normal'

        rectBtnActive(widget)