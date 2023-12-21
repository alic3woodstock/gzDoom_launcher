from kivy.graphics import Callback
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButtonBehavior

from gameDef import GameDef
from gameGrid import GameGrid
from gridContainer import GridContainer
from myButton import MyButtonBorder, DropdownItem
from functions import button_height
from myLayout import MyStackLayout


class GameCarousel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        topPanel = MyStackLayout()
        topPanel.size_hint = (1, None)
        topPanel.height = 64
        topPanel.padding = (8, 18, 8, 0)
        carousel = MyCarousel()
        carousel.anim_move_duration = 0.3
        spinnerBox = BoxLayout()
        spinnerBox.padding = [7, 0, 15, 16]
        spinnerBox.size_hint = (1, None)
        spinnerBox.height = button_height + spinnerBox.padding[3]
        label = Label(text='Mod:')
        label.size_hint = (None, 1)
        print(label.texture_size)
        spinnerBox.add_widget(label)
        dropDown = DropDown()
        dropDown.size_hint = (1, None)
        dropDown.sync_height = True
        dropDown.height = button_height
        dropDown.bind(on_select=self.dropDown_on_select)
        dropDown.bind(on_dismiss=self.dropDown_on_dismiss)
        mainBtnDrop = MainModButton(game=GameDef(0, '-- None --', -1), text='None',
                                    height=button_height)
        mainBtnDrop.bind(on_release=dropDown.open)
        self.noMod = mainBtnDrop.game
        self.modList = []
        spinnerBox.add_widget(mainBtnDrop)
        self.orientation = 'vertical'
        self.add_widget(topPanel)
        self.add_widget(carousel)
        self.add_widget(spinnerBox)
        self.carousel = carousel
        self.topPanel = topPanel
        self.dropDown = dropDown
        self.mainBtnDrop = mainBtnDrop

    def add_tab(self, name, tabId=0):
        index = len(self.carousel.slides)
        btnTitle = CarouselButton(index)
        btnTitle.text = name
        btnTitle.width = 200
        btnTitle.bind(state=self.btnTitle_on_state)
        btnTitle.bind(on_press=self.btnTitle_on_press)
        self.topPanel.add_widget(btnTitle)

        gameGrid = GridContainer(GameGrid())
        gameGrid.container.size_hint = (1, 1)
        gameGrid.grid.on_change_selection = self.grid_on_change_selection

        gameTab = GameTab(tabId, tabId, btnTitle, gameGrid)
        self.carousel.add_widget(gameTab)

    def select_tab(self, tabId):
        for gameTab in self.carousel.slides:
            if gameTab.tabId == tabId:
                gameTab.btnTitle.state = 'down'
                self.carousel.on_index()

    def insert_game(self, game=None):
        if game:
            if game.tab < 0:
                self.modList.append(game)
                self.modList.sort(key=self.list_sort)
            else:
                for gameTab in self.carousel.slides:
                    if gameTab.tabId == game.tab:
                        gameTab.gameGrid.grid.insert_game(game)

    def list_sort(self, game):
        return game.name

    def clear_tabs(self):
        self.carousel.clear_widgets()
        self.topPanel.clear_widgets()

    def btnTitle_on_state(self, widget, state):
        if widget.state == 'down':
            for c in self.topPanel.children:
                if c != widget:
                    c.state = 'normal'
            self.carousel.load_slide(self.carousel.slides[widget.tabIndex])
            # print(self.dropDown.children)

    def btnTitle_on_press(self, widget):
        if widget.state == 'normal':
            widget.state = 'down'

    def btnDrop_on_press(self, widget):
        self.dropDown.select(widget.game)

    def dropDown_on_select(self, widget, data):
        self.mainBtnDrop.text = data.name
        self.mainBtnDrop.game = data
        self.mainBtnDrop.state = 'normal'

    def dropDown_on_dismiss(self, widget):
        self.mainBtnDrop.state = 'normal'

    def grid_on_change_selection(self, widget):
        self.dropDown.clear_widgets()

        modButton = ModButton(self.noMod)
        modButton.bind(on_press=self.btnDrop_on_press)
        self.dropDown.add_widget(modButton)

        if widget:
            for game in self.modList:
                if game.group.GetGroupId() == widget.game.group.GetGroupId():
                    modButton = ModButton(game)
                    modButton.bind(on_press=self.btnDrop_on_press)
                    self.dropDown.add_widget(modButton)

            if widget.game.lastMod > 0:
                for game in self.modList:
                    if game.id == widget.game.lastMod:
                        self.mainBtnDrop.game = game
                        self.mainBtnDrop.text = game.name
                        return

        self.mainBtnDrop.game = self.noMod
        self.mainBtnDrop.text = self.noMod.name
        return

    def spacebar(self):
        gameCount = len(self.dropDown.children[0].children)
        for i in range(gameCount):
            btn = self.dropDown.children[0].children
            if btn[i].game.id == self.mainBtnDrop.game.id:
                if i > 0:
                    self.dropDown.select(btn[i - 1].game)
                else:
                    self.dropDown.select(btn[gameCount - 1].game)
                return

    def get_run_params(self):
        return [self.carousel.current_slide.gameGrid.grid.get_game(), self.mainBtnDrop.game]


class CarouselButton(ToggleButtonBehavior, MyButtonBorder):

    def __init__(self, tabIndex, **kwargs):
        super().__init__(**kwargs)
        self.tabIndex = tabIndex
        self.size_hint = (None, 1)
        self.highlight_color = self.text_color
        self.canvas.add(Callback(self.update_button))

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
        self.canvas.after.clear()
        self.draw_button()
        self.draw_border()
        self.canvas.ask_update()


class GameTab(BoxLayout):
    def __init__(self, tabId, tabIndex=0, btnTitle=None, grid=None, **kwargs):
        super().__init__(**kwargs)
        self.lineWidth = 1
        self.padding = 16
        self.tabId = tabId  # tab id in database
        self.tabIndex = tabIndex  # tab index in carousel
        self.btnTitle = btnTitle
        self.gameGrid = grid
        self.add_widget(grid)


class MyCarousel(Carousel):

    def on_index(self, *args):
        super().on_index(*args)
        if self.current_slide:
            self.parent.grid_on_change_selection(self.current_slide.gameGrid.grid.get_game_btn())
            self.current_slide.btnTitle.state = 'down'


class ModButton(MyButtonBorder):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.height = button_height
        if game:
            self.text = game.name


class MainModButton(DropdownItem):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.height = button_height
        if game:
            self.text = game.name
