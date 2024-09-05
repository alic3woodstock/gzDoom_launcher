import os
from os import listdir
from os.path import isdir
from shutil import copy

from kivy.core.window import Window

from configDB import write_config, read_config
from dataPath import data_path
from functions import button_height
from gameDef import GameDef
from gameDefDB import insert_game, delete_games_from_tab
from gameFileFunctions import GameFileFunctions
from gameTab import GameTab
from gameTabDB import select_all_game_tabs, update_all_game_tabs
from genericForm import GenericForm
from myPopup import MyPopup, ModalWindow, MessageBox
from url import Url


class FrmImportDoom(ModalWindow):

    def __init__(self, dialog, **kwargs):
        super().__init__(dialog, **kwargs)
        self.popup = MyPopup()
        self.genericForm = GenericForm()
        text = 'Doom + Doom II path:'
        self.genericForm.add_file_field(text, 'file', True)
        self.genericForm.add_checkbox_field('Use remix tracks', 'remix')
        self.add_widget(self.genericForm)

        self.genericForm.ids.remix.active = True

        self.create_box_buttons(
            'OK', 'Cancel')
        self.btnOk.bind(on_release=self.btn_ok_on_press)
        self.dialog.height = (button_height * 2  # box buttons height + tithe height
                              + self.genericForm.get_height())

    def btn_ok_on_press(self, _widget):
        msg = MessageBox()
        if os.name == 'nt':
            file = self.genericForm.ids.file.text.strip() + '\\'
        else:
            file = self.genericForm.ids.file.text.strip() + '/'
        if not isdir(file):
            msg.alert('Invalid path!')
        else:
            if os.name == 'nt':
                file = self.genericForm.ids.file.text.strip() + '\\'
            else:
                file = self.genericForm.ids.file.text.strip() + '/'

            files = listdir(file.strip())
            games = []
            tabs = select_all_game_tabs()
            free_id = read_config('doom2024tab', 'num')
            if free_id <= 0:
                for t in tabs:
                    if t.index == free_id:
                        free_id += 1

            if free_id > 9:
                msg.alert("Can't create a new tab!")
            else:
                doomwad = ''
                doom2wad = ''
                extraswad = ''
                id1wad = ''
                id24reswad = ''
                id1reswad = ''
                id1weapwad = ''
                for f in files:
                    if f.lower() == 'doom.wad':
                        doomwad = file + f
                        games.append(GameDef(0, 'Doom', free_id,
                                             data_path().gzDoomExec, 1, 0, doomwad))
                    if f.lower() == 'doom2.wad':
                        doom2wad = file + f
                        games.append(GameDef(0, 'Doom II: Hell on Earth', free_id,
                                             data_path().gzDoomExec, 1, 0, doom2wad))
                if not doomwad.strip():
                    msg.alert('Doom.wad not found!')
                elif not doom2wad.strip():
                    msg.alert('Doom2.wad not found!')
                else:
                    for f in files:
                        if f.lower() == 'masterlevels.wad':
                            games.append(GameDef(0, 'Master Levels for Doom II', free_id,
                                                 data_path().gzDoomExec, 1, 0, doom2wad,
                                                 [file + f]))
                        if f.lower() == 'tnt.wad':
                            games.append(GameDef(0, 'TNT: Evolution', free_id,
                                                 data_path().gzDoomExec, 1, 0, file + f))
                        if f.lower() == 'plutonia.wad':
                            games.append(GameDef(0, 'The Plutonia Experiment', free_id,
                                                 data_path().gzDoomExec, 1, 0, file + f))
                        if f.lower() == 'nerve.wad':
                            games.append(GameDef(0, 'No Rest for the Living', free_id,
                                                 data_path().gzDoomExec, 1, 0, doom2wad,
                                                 [file + f]))
                        if f.lower() == 'sigil.wad':
                            games.append(GameDef(0, 'Sigil', free_id,
                                                 data_path().gzDoomExec, 1, 0, doomwad,
                                                 [file + f]))
                        if f.lower() == 'extras.wad':
                            extraswad = file + f
                        if f.lower() == 'id1.wad':
                            id1wad = file + f
                        if f.lower() == 'id24res.wad':
                            id24reswad = file + f
                        if f.lower() == 'id1-res.wad':
                            id1reswad = file + f
                        if f.lower() == 'id1-weap.wad':
                            id1weapwad = file + f

                    if (id1wad.strip() and id24reswad.strip() and id1reswad.strip() and
                            id1weapwad.strip()):
                        games.append(GameDef(0, 'Legacy of Rust', free_id,
                                             data_path().gzDoomExec, 1, 0, doom2wad,
                                             [id1wad.strip(), id24reswad.strip(), id1reswad.strip(),
                                              id1weapwad.strip()]))
                    if extraswad.strip():
                        for g in games:
                            g.files.append(extraswad.strip())

                    if len(games) < 8:
                        msg.alert('Invalid Doom + Doom2 release!')
                    else:
                        can_save = True
                        if self.genericForm.ids.remix.active:
                            try:
                                game_file = GameFileFunctions()
                                game_file.totalDownloads = 1
                                gzde_file_name = 'gzd-extras-sndinfos-v2.pk3'
                                url = Url('https://forum.zdoom.org/download/file.php?id=45740',
                                          gzde_file_name)
                                game_file.download_file(url)
                                copy(data_path().download + gzde_file_name,
                                     data_path().mod + gzde_file_name)
                                for g in games:
                                    g.files.append(data_path().mod + 'gzd-extras-sndinfos-v2.pk3')
                            except Exception as e:
                                can_save = False
                                msg.alert('Error downloading remix patch: ' + str(e) + '!')

                        if can_save:
                            tab_found = False
                            for t in tabs:
                                if t.index == free_id:
                                    t.name = 'DOOM + DOOM II'
                                    t.is_enabled = True
                                    tab_found = True
                            if not tab_found:
                                tabs.append(GameTab(free_id, 'DOOM + DOOM II', True))
                            delete_games_from_tab(free_id)
                            update_all_game_tabs(tabs)
                            write_config('doom2024tab', free_id, 'num')

                            for g in games:
                                insert_game(g)

                            msg.message('DOOM + DOOM II 2024 successfully imported.', 'information')
                            self.dialog.dismiss()
