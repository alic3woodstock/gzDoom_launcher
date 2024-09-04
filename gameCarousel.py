from kivy.graphics import Callback
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButtonBehavior

from functions import button_height
from gameDef import GameDef
from gameGrid import GameGrid
from gridContainer import GridContainer
from myButton import MyButtonBorder, DropdownMainButton, DropDownItem
from myDropdown import MyDropdown
from myLayout import MyStackLayout


def list_sort(game):
    return game.name


def btn_title_on_press(widget):
    if widget.state == 'normal':
        widget.state = 'down'


class GameCarousel(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        top_panel = MyStackLayout()
        top_panel.size_hint = (1, None)
        top_panel.height = 64
        top_panel.padding = (8, 18, 8, 0)
        carousel = MyCarousel()
        carousel.anim_move_duration = 0.3
        spinner_box = BoxLayout()
        spinner_box.padding = [7, 0, 15, 16]
        spinner_box.size_hint = (1, None)
        spinner_box.height = button_height + spinner_box.padding[3]
        label = Label(text='Mod:')
        label.size_hint = (None, 1)

        spinner_box.add_widget(label)
        main_btn_drop = MainModButton(game=GameDef(0, '-- None --', -1), text='None',
                                      height=button_height)

        drop_down = MyDropdown(main_btn_drop)
        drop_down.size_hint = (1, None)
        drop_down.sync_height = True
        drop_down.height = button_height

        self.noMod = main_btn_drop.game
        self.modList = []
        spinner_box.add_widget(main_btn_drop)
        self.orientation = 'vertical'
        self.add_widget(top_panel)
        self.add_widget(carousel)
        self.add_widget(spinner_box)
        self.carousel = carousel
        self.topPanel = top_panel
        self.dropDown = drop_down
        self.mainBtnDrop = main_btn_drop

    def add_tab(self, name, tab_id=0):
        index = len(self.carousel.slides)
        btn_title = CarouselButton(index)
        btn_title.text = name
        btn_title.width = 200
        btn_title.bind(state=self.btn_title_on_state)
        btn_title.bind(on_press=btn_title_on_press)
        self.topPanel.add_widget(btn_title)

        game_grid = GridContainer(GameGrid())
        game_grid.container.size_hint = (1, 1)
        game_grid.grid.on_change_selection = self.grid_on_change_selection

        game_tab = GameCarouselTab(tab_id, tab_id, btn_title, game_grid)
        self.carousel.add_widget(game_tab)

    def select_tab(self, tab_id):
        for gameTab in self.carousel.slides:
            if gameTab.tabId == tab_id:
                gameTab.btnTitle.state = 'down'
                self.carousel.on_index()

    def insert_game(self, game=None):
        if game:
            if game.tabId < 0:
                self.modList.append(game)
                self.modList.sort(key=list_sort)
            else:
                for gameTab in self.carousel.slides:
                    if gameTab.tabId == game.tabId:
                        gameTab.gameGrid.grid.insert_game(game)

    def clear_tabs(self):
        self.carousel.clear_widgets()
        self.topPanel.clear_widgets()
        self.modList = []

    def btn_title_on_state(self, widget, value):
        if value == 'down':
            for c in self.topPanel.children:
                if c != widget:
                    c.state = 'normal'
            self.carousel.load_slide(self.carousel.slides[widget.tabIndex])
            # print(self.dropDown.children)

    def grid_on_change_selection(self, widget):
        self.dropDown.clear_widgets()

        mod_button = DropDownItem(self.noMod)
        self.dropDown.add_widget(mod_button)

        if widget:
            for game in self.modList:
                if game.group.id == widget.game.group.id:
                    mod_button = DropDownItem(game)
                    self.dropDown.add_widget(mod_button)

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
        game_count = len(self.dropDown.children[0].children)
        for i in range(game_count):
            btn = self.dropDown.children[0].children
            if btn[i].game.id == self.mainBtnDrop.game.id:
                if i > 0:
                    self.dropDown.select(btn[i - 1].game)
                else:
                    self.dropDown.select(btn[game_count - 1].game)
                return

    def get_run_params(self):
        return [self.carousel.current_slide.gameGrid.grid.get_game(), self.mainBtnDrop.game]

    def update_current_game(self, game):
        game_btn = self.carousel.current_slide.gameGrid.grid.get_game_btn()
        game_btn.game = game


class CarouselButton(ToggleButtonBehavior, MyButtonBorder):

    def __init__(self, tab_index, **kwargs):
        super().__init__(**kwargs)
        self.tabIndex = tab_index
        self.size_hint = (None, 1)
        self.highlight_color = self.text_color
        self.canvas.add(Callback(self.update_button))

    def update_button(self, instr):
        self.width = self.texture_size[0] + 16
        self.canvas.after.clear()
        self.draw_button()
        self.draw_border()
        self.canvas.ask_update()


class GameCarouselTab(BoxLayout):
    def __init__(self, tab_id, tab_index=0, btn_title=None, grid=None, **kwargs):
        super().__init__(**kwargs)
        self.lineWidth = 1
        self.padding = 16
        self.tabId = tab_id  # tab id in database
        self.tabIndex = tab_index  # tab index in carousel
        self.btnTitle = btn_title
        self.gameGrid = grid
        self.add_widget(grid)


class MyCarousel(Carousel):

    def on_index(self, *args):
        super().on_index(*args)
        if self.current_slide:
            self.parent.grid_on_change_selection(self.current_slide.gameGrid.grid.get_game_btn())
            self.current_slide.btnTitle.state = 'down'


class MainModButton(DropdownMainButton):
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.height = button_height
        if game:
            self.text = game.name
