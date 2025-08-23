import os
import shutil

from kivy.core.window import Window
from kivy.graphics import Callback
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from configDB import read_config, write_config
from functions import button_height, set_language, log
from gameTab import GameTab
from gameTabDB import select_all_game_tabs, update_all_game_tabs
from genericForm import GenericForm
from gridContainer import GridContainer
from myButton import DropDownItem
from myLayout import MyAnchorLayout, MyBoxLayout
from myPopup import ModalWindow, MessageBox


class FrmSettings(ModalWindow):
    def __init__(self, dialog, temp_locale=None, **kwargs):
        super().__init__(dialog, **kwargs)
        self.genericForm = GenericForm()

        layout1 = self.anchor_layout()
        layout1.borders = []
        self.label_tabs = Label(text=_('Configure Tabs:'))
        self.label_tabs.size_hint = (None, None)
        self.label_tabs.halign = 'left'
        self.label_tabs.valign = 'middle'
        self.label_tabs.height = self.genericForm.children_height
        layout1.add_widget(self.label_tabs)

        self.genericForm.topLayout.padding = [16, 0, 16, 16]
        for i in range(1, 10):
            field_name = 'tab' + str(i)
            text = _('Tab') + ' ' + str(i) + ':'
            self.genericForm.add_checkbox_input(text, field_name)

        game_tabs = select_all_game_tabs()
        for g in game_tabs:
            if g.index >= 0:
                field_name = 'tab' + str(g.index + 1) + '_check'
                self.genericForm.ids[field_name].active = g.is_enabled
                field_name = 'tab' + str(g.index + 1) + '_name'
                self.genericForm.ids[field_name].text = g.name

        layout2 = MyBoxLayout()
        layout2.size_hint = [1, None]
        layout2.borders = ['top']

        self.genericForm2 = GenericForm()
        self.genericForm2.add_dropdown(_('Language:'), 'language')
        language = [LanguageOpt('en', 'English'), LanguageOpt('pt_BR', 'Português do Brasil')]

        for l in language:
            self.genericForm2.ids.language.add_widget(DropDownItem(l))

        if not temp_locale:
            temp_locale = read_config("language", "text")

        for l in language:
            if l.locale == temp_locale:
                self.genericForm2.ids.language.select(l)
                break

        self.genericForm2.ids.language.bind(on_select=self.on_language_select)

        if os.name != 'nt':
            self.genericForm2.add_file_field(_("Custom wine binary:"), "winecommand", False)
            self.genericForm2.ids.winecommand.text = read_config("winecommand", "text")

        self.genericForm2.add_checkbox_field(_('Check for GZDoom updates on startup'), 'chkupdate')
        self.genericForm2.ids.chkupdate.active = read_config('checkupdate', 'bool')

        layout2.height = self.genericForm2.get_height() - 16
        layout2.add_widget(self.genericForm2)

        form_height = self.genericForm.get_height() + layout1.height + layout2.height + 4

        top_box = BoxLayout()
        top_box.size_hint = (1, None)
        top_box.height = form_height
        top_box.orientation = 'vertical'
        top_box.add_widget(layout1)
        top_box.add_widget(self.genericForm)
        top_box.add_widget(layout2)
        top_layout = GridContainer(top_box)
        top_layout.padding = 0
        top_layout.container.size_hint = (1, 1)
        top_layout.borders = []
        self.add_widget(top_layout)

        self.create_box_buttons(
            'OK', _('Cancel'))
        self.btnOk.bind(on_release=self.btn_ok_on_press)

        form_height += button_height * 2  # box buttons height + title height

        if form_height > Window.height:
            self.dialog.height = Window.height
        else:
            self.dialog.height = form_height
        self.canvas.add(Callback(self.update_form))

    def update_form(self, _instr):
        self.label_tabs.size = self.label_tabs.texture_size

    def anchor_layout(self):
        layout = MyAnchorLayout()
        layout.size_hint = (1, None)
        layout.padding = 16
        layout.spacing = self.genericForm.topLayout.spacing[0]
        layout.height = self.genericForm.get_height()
        layout.anchor_x = 'left'
        layout.anchor_y = 'center'
        return layout

    def btn_ok_on_press(self, _widget):
        has_active_tab = False
        empty_text = False
        for i in range(1, 10):
            if self.genericForm.ids['tab' + str(i) + '_check'].active:
                has_active_tab = True
            if (self.genericForm.ids['tab' + str(i) + '_check'].active
                    and not self.genericForm.ids['tab' + str(i) + '_name'].text.strip()):
                empty_text = True

        wine_ok = True
        winecmd = ""
        if os.name != 'nt':
            wine_ok = False
            winecmd = self.genericForm2.ids.winecommand.text.strip()
            if winecmd:
                try:
                    if os.path.isfile(winecmd) and shutil.which(winecmd):
                        wine_ok = True
                except Exception as e:
                    log(str(e), True)
                    wine_ok = False
            else:
                wine_ok = True

        msg = MessageBox()
        if not has_active_tab:
            msg.alert(_('At least one tab has to be enabled!'))
        elif empty_text:
            msg.alert(_('Enabled tabs must have a description!'))
        elif not wine_ok:
            msg.alert(_("Invalid wine binary!"))
        else:
            old_locale = read_config("language", "text")
            new_locale = self.genericForm2.ids.language.main_button.game.locale
            if old_locale != new_locale:
                write_config("language", new_locale, "text")
                try:
                    Window.children[1].clear_widgets()
                    Window.children[1].__init__()
                finally:
                    pass

            game_tabs = []
            for i in range(0, 9):
                index = i
                name = self.genericForm.ids['tab' + str(i + 1) + '_name'].text.strip()
                is_enabled = self.genericForm.ids['tab' + str(i + 1) + '_check'].active
                game_tabs.append(GameTab(index, name, is_enabled))

            update_all_game_tabs(game_tabs)
            write_config('checkupdate', self.genericForm2.ids.chkupdate.active, 'bool')
            write_config("winecommand", winecmd, "text")
            self.dialog.dismiss()

    def on_language_select(self, _widget, data):
        set_language(data.locale)
        self.__init__(self.dialog, data.locale)


class LanguageOpt:

    def __init__(self, locale='en', name='English'):
        self.id = 0
        self.locale = locale
        self.name = name
