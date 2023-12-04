from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Line, Callback, Rectangle
from kivy.uix.label import CoreLabel
from myLayout import MyStackLayout
from kivyFunctions import border_color, normal_color, GetBorders
from gameGrid import GameGrid
from gameDefDb import GameDefDb

class GameCarousel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        topPanel = MyStackLayout()
        topPanel.size_hint = (1, None)
        topPanel.height = 64
        topPanel.padding = (8, 18, 8, 0)
        carousel = MyCarousel()
        carousel.anim_move_duration = 0.3
        self.orientation = 'vertical'
        self.add_widget(topPanel)
        self.add_widget(carousel)
        self.carousel = carousel
        self.topPanel = topPanel
        self.gameTabs = []

    def add_tab(self, name, tabId=0):
        index = len(self.gameTabs)
        btnTitle = CarouselButton(index)
        btnTitle.text = name
        btnTitle.width = 200
        btnTitle.bind(state=self.btnTitle_on_state)
        btnTitle.bind(on_press=self.btnTitle_on_press)
        self.topPanel.add_widget(btnTitle)
        gameGrid = GameGrid()
        self.carousel.add_widget(gameGrid)
        self.gameTabs.append(GameTab(tabId, tabId, btnTitle, gameGrid))

    def select_tab(self, tabId):
        for gameTab in self.gameTabs:
            if gameTab.tabId == tabId:
                gameTab.btnTitle.state = 'down'

    def insert_game(self, game=None):
        if game:
            for gameTab in self.gameTabs:
                if gameTab.tabId == game.tab:
                    gameTab.gameGrid.insert_game(game)

    def clear_tabs(self):
        self.gameTabs.clear()


    def btnTitle_on_state(self, widget, state):
        if widget.state == 'down':
            for c in self.topPanel.children:
                if c != widget:
                    c.state = 'normal'
            self.carousel.load_slide(self.gameTabs[widget.tabIndex].gameGrid)

    def btnTitle_on_press(self, widget):
        if widget.state == 'normal':
            widget.state = 'down'

class CarouselButton(ToggleButton):

    def __init__(self, tabIndex, **kwargs):
        super().__init__(**kwargs)
        self.tabIndex = tabIndex
        self.size_hint = (None, 1)
        self.canvas.add(Callback(self.update_button))

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
        self.canvas.after.clear()
        self.change_color()
        self.canvas.ask_update()

    def change_color(self):
        padding = [8, self.height / 2 - self.texture_size[1] / 2]
        label = CoreLabel(text=self.text, color=normal_color,
                          font_size=self.font_size, font=self.font_name,
                          halign='center', valign='center', padding=padding)
        label.refresh()
        if self.state == 'normal':
            self.background_color = normal_color
            self.color = border_color
            borders = GetBorders(self)
            with self.canvas.after:
                Color(border_color)
                Line(points=[borders.top_left, borders.bottom_left, borders.bottom_right, borders.top_right],
                     width=1)
        else:
            self.background_color = border_color
            self.color = normal_color
            with self.canvas.after:
                Color(border_color)
                Rectangle(pos=self.pos, size=(self.width, self.height + 1))
                Color(normal_color)
                text = label.texture
                Rectangle(pos=self.pos, size=self.size, texture=text)

class GameTab():
    def __init__(self, tabId, tabIndex=0, btnTitle=None, grid=None):
        self.tabId = tabId # tab id in database
        self.tabIndex = tabIndex # tab index in carousel
        self.btnTitle = btnTitle
        self.gameGrid = grid
        
class MyCarousel(Carousel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_index(self, *args):
        super().on_index(*args)
        if self.parent.gameTabs and len(self.parent.gameTabs) > args[1]:
            tab = self.parent.gameTabs[args[1]]
            if tab.btnTitle.state == 'normal':
                tab.btnTitle.state = 'down'
