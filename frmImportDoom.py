import os
from os.path import isdir
from os.path import isfile
from functions import log
from shutil import copy, rmtree
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
        folder_char = '/'
        if os.name == 'nt':
            folder_char = '\\'

        file = self.genericForm.ids.file.text.strip() + folder_char
        if not isdir(file):
            msg.alert('Invalid path!')
        else:
            file = self.genericForm.ids.file.text.strip() + folder_char

            files = os.listdir(file.strip())
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
                can_save = True

                tmp_folder = data_path().data + folder_char + 'doom2024_tmp'
                doom_folder = data_path().data + folder_char + 'doom2024' + folder_char
                try:
                    if isdir(tmp_folder):
                        rmtree(tmp_folder)
                    os.mkdir(tmp_folder)
                except Exception as e:
                    log(e)
                    msg.alert("Can't create doom2024 temp folder!")
                    can_save = False

                if can_save:
                    for f in files:
                        copy(file + f, tmp_folder)

                        if f.lower() == 'doom.wad':
                            doomwad = doom_folder + f
                            # games.append(GameDef(0, 'Doom', free_id,
                            #                      data_path().gzDoomExec, 1, 0, doomwad))
                        if f.lower() == 'doom2.wad':
                            doom2wad = doom_folder + f

                    if not doomwad.strip():
                        msg.alert('Doom.wad not found!')
                    elif not doom2wad.strip():
                        msg.alert('Doom2.wad not found!')
                    else:
                        for f in files:
                            if f.lower() == 'sigil.wad':
                                if isfile(data_path().map + 'sigil2.zip'):
                                    games.append(GameDef(0, 'Doom + Sigil + Sigil II', free_id,
                                                         data_path().gzDoomExec, 1, 0, doomwad,
                                                         [doom_folder + f, data_path().map + 'sigil2.zip']))
                                else:
                                    games.append(GameDef(0, 'Doom + Sigil', free_id,
                                                         data_path().gzDoomExec, 1, 0, doomwad,
                                                         [doom_folder + f]))
                            if f.lower() == 'doom2.wad':
                                games.append(GameDef(0, 'Doom II: Hell on Earth', free_id,
                                                     data_path().gzDoomExec, 1, 0, doom2wad))

                            if f.lower() == 'masterlevels.wad':
                                games.append(GameDef(0, 'Master Levels for Doom II', free_id,
                                                     data_path().gzDoomExec, 1, 0, doom2wad,
                                                     [doom_folder + f]))
                            if f.lower() == 'tnt.wad':
                                games.append(GameDef(0, 'TNT: Evolution', free_id,
                                                     data_path().gzDoomExec, 1, 0, doom_folder + f))
                            if f.lower() == 'plutonia.wad':
                                games.append(GameDef(0, 'The Plutonia Experiment', free_id,
                                                     data_path().gzDoomExec, 1, 0, doom_folder + f))
                            if f.lower() == 'nerve.wad':
                                games.append(GameDef(0, 'No Rest for the Living', free_id,
                                                     data_path().gzDoomExec, 1, 0, doom2wad,
                                                     [doom_folder + f]))
                            if f.lower() == 'extras.wad':
                                extraswad = doom_folder + f
                            if f.lower() == 'id1.wad':
                                id1wad = doom_folder + f
                            if f.lower() == 'id24res.wad':
                                id24reswad = doom_folder + f
                            if f.lower() == 'id1-res.wad':
                                id1reswad = doom_folder + f
                            if f.lower() == 'id1-weap.wad':
                                id1weapwad = doom_folder + f

                        if (id1wad.strip() and id24reswad.strip() and id1reswad.strip() and
                                id1weapwad.strip()):
                            games.append(GameDef(0, 'Legacy of Rust', free_id,
                                                 data_path().gzDoomExec, 1, 0, doom2wad,
                                                 [id1wad.strip(), id24reswad.strip(), id1reswad.strip(),
                                                  id1weapwad.strip()]))
                        if extraswad.strip():
                            for g in games:
                                g.files.append(extraswad.strip())

                        if len(games) < 7:
                            msg.alert('Invalid Doom + Doom2 release!')
                        else:
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
                                try:
                                    doom_folder = data_path().data + folder_char + 'doom2024'

                                    if isdir(doom_folder):
                                        os.rename(doom_folder, doom_folder + '_bak')

                                    os.rename(tmp_folder, doom_folder)

                                    if isdir(doom_folder + '_bak'):
                                        rmtree(doom_folder + '_bak')
                                except Exception as e:
                                    log(e)
                                    msg.alert('Error creating doom 2024 folder!')
                                    can_save = False

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
