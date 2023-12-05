import math

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from myLayout import MyBoxLayout
from kivyFunctions import change_color

button_height = 42

class GameButton(ToggleButton):
    def __init__(self, game=None, **kwargs):
        super(ToggleButton, self).__init__(**kwargs)
        self.game = game
        self.size_hint = (1, None)


class GameGrid(MyBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.games = []
        self.lineWidth = 1

        self.scroll = ScrollView()
        self.scroll.bar_width = 4
        self.container = StackLayout()
        self.container.orientation = 'bt-lr'
        self.container.size_hint = (1, None)
        self.container.height = 0
        self.scroll.add_widget(self.container)
        self.add_widget(self.scroll)
        # kivyFunctions.change_color(self, use_alternative_color=True)

    def insert_game(self, game=None):
        gameButton = GameButton(game, text=game.name)
        self.container.add_widget(gameButton)
        gameButton.height = button_height
        self.container.height += gameButton.height
        gameButton.bind(state=self.btnCfg_on_state)
        gameButton.bind(on_press=self.btnCfg_on_press)
        # self.background_color = [0, 0, 0, 0]
        change_color(gameButton)
        gameButton.state = 'down'

    def btnCfg_on_state(self, widget, state):
        if widget.state == 'down':
            # print(widget.y, self.container.height - self.height)
            if self.container.height > self.height:
                self.scroll.scroll_to(widget, padding=0)
            for c in self.container.children:
                if c != widget:
                    c.state = 'normal'
            self.on_change_selection(widget)

        change_color(widget)


    def btnCfg_on_press(self, widget):
        if widget.state == 'normal':
            widget.state = 'down'

    def on_change_selection(self, widget):
        pass


    def get_game_btn(self):
        for gameBtn in self.container.children:
            if gameBtn.state == 'down':
                return gameBtn

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
        if index < (len(self.container.children)):
            self.select_game_index(index + 1)

    def load_previous_game(self):
        index = self.get_index()
        if index > 0:
            self.select_game_index(index - 1)

    def page_down(self):
        sBottom = self.scroll.viewport_size[1] / button_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / button_height)
        if sBottom <= 0:
            self.select_game_index(len(self.container.children) - 1)
        else:
            index = self.get_index()
            index2 = len(self.container.children) - sBottom - 1
            if index == index2:
                if (sBottom < qtdByView):
                    self.select_game_index(len(self.container.children) - 1)
                else:
                    self.select_game_index(index + qtdByView)
            else:
                self.select_game_index(index2)

    def page_up(self):
        sBottom = self.scroll.viewport_size[1] / button_height
        sBottom = round(self.scroll.vbar[0] * sBottom)
        qtdByView = round(self.scroll.height / button_height)
        sTop = len(self.container.children) - sBottom - qtdByView
        if sTop <= 0:
            self.select_game_index(0)
        else:
            index = self.get_index()
            if index == sTop:
                if sTop >= qtdByView:
                    self.select_game_index(sTop - qtdByView)
                else:
                    self.select_game_index(0)
            else:
                self.select_game_index(sTop)
