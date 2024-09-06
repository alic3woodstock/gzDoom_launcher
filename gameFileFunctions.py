import math
import os
import shutil
from tarfile import open as TarFile
from zipfile import ZipFile

from kivy.clock import Clock
from py7zr import SevenZipFile

from configDB import update_gzdoom_version, read_config, write_config
from createDB import create_game_table
from dataPath import data_path
from functions import (log as write_log, filehash, WINE_GZDOOM, RE_DOWNLOAD, log)
from gameDef import GameDef
from gameDefDB import delete_game_table, insert_game
from gzdoomUpdate import GZDoomUpdate
from url import Url
from urlDB import insert_default_urls, select_default_urls


def create_db():
    check_update = True
    try:
        if os.path.isfile(data_path().db):
            check_update = read_config('checkupdate', 'bool')
    except Exception as e:
        write_log(e)

    delete_game_table()
    create_game_table()
    write_config('checkupdate', check_update, 'bool')

    game_files = []
    games = []

    wads = os.listdir(data_path().wad)
    for w in wads:
        game_files.append(
            GameFile(w, data_path().wad))  # store path in format string since I don't need to use Extract

    maps = os.listdir(data_path().map)
    for a in maps:
        game_files.append(GameFile(a, data_path().map))

    mods = os.listdir(data_path().mod)
    for m in mods:
        game_files.append(GameFile(m, data_path().mod))

    blasphem_wad = ""
    blasphem_texture = ""

    game_exec = data_path().gzDoomExec

    i = 0
    for z in game_files:
        try:
            full_path = z.get_format() + z.get_name()

            if z.test_file_name("blasphem"):
                blasphem_wad = full_path
            elif z.test_file_name("bls"):
                blasphem_texture = full_path
            elif z.test_file_name("freedoom1"):
                games.append(GameDef(i, "Freedoom Phase 1", 0, game_exec, 1, 0, full_path))
            elif z.test_file_name("freedoom2"):
                games.append(GameDef(i, "Freedoom Phase 2", 0, game_exec, 1, 0, full_path))
            elif z.test_file_name("harmonyc.wad"):
                games.append(GameDef(i, 'Harmony', 0, game_exec, 5, 0,
                                     full_path,
                                     [z.get_format() + 'HarmonyC.deh',
                                      z.get_format() + 'Harm-WS.wad']))
            elif z.get_format().find("maps") >= 0:
                if z.test_file_name("htchest") or z.test_file_name("unbeliev"):
                    games.append(GameDef(i, z.get_map_name(), 1, game_exec, 2, 0,
                                         data_path().wad + "blasphem.wad",
                                         [data_path().wad + "BLSMPTXT.WAD", full_path]))
                else:
                    games.append(GameDef(i, z.get_map_name(), 1, game_exec, 1, 0,
                                         data_path().wad + "freedoom2.wad", [full_path]))
            elif z.get_format().find("mods") >= 0:
                if z.test_file_name("150skins"):
                    games.append(
                        GameDef(i, "150 Skins", -1, '', 2, 0,  # 150 Skins also works with heretic
                                "", [full_path]))
                    games.append(
                        GameDef(i, "150 Skins", -1, '', 1, 0,  # 150 Skins also works with heretic
                                "", [full_path]))
                elif z.test_file_name("beautiful"):
                    games.append(GameDef(i, "Beautiful Doom", -1, '', 1, 0,
                                         "", [data_path().mod + "150skins.zip", full_path]))
                elif z.test_file_name("brutal"):
                    games.append(GameDef(i, "Brutal Doom", -1, '', 1, 0,
                                         "", [full_path]))
                elif z.test_file_name("evp") and z.test_file_name("pk3"):
                    games.append(GameDef(i, "Enhanced Vanilla Project", -1, '', 1, 0,
                                         "", [data_path().mod + "150skins.zip", full_path]))
                elif z.test_file_name("cats"):
                    games.append(GameDef(i, "Space Cats Saga", 0, game_exec, 5, 0,
                                         data_path().wad + "freedoom2.wad", [full_path]))
                    i += 1
                    games.append(GameDef(i, "Space Cats Saga", -1, '', 1, 0,
                                         "", [full_path]))

            if blasphem_wad.strip() and blasphem_texture.strip():  # insert game only if both files are ok
                games.append(GameDef(i, "Blasphem", 0, game_exec, 2, 0, blasphem_wad, [blasphem_texture]))
                blasphem_wad = ""
                blasphem_texture = ""

        except Exception as e:
            write_log("CreateDB - " + str(e))

        i += 1

    for g in games:
        insert_game(g)


class GameFileFunctions:
    def __init__(self):
        self.value = 0
        self.message = 'Starting ...'
        self.max_range = 100
        self.clock = None
        self.totalDownloads = 0
        self.currentDownload = 0
        self.done = False

    def extract_all(self):
        self.done = False
        self.message = 'Downloading files...'

        if RE_DOWNLOAD:
            shutil.rmtree(data_path().download)

        if not os.path.exists(data_path().download):
            os.mkdir(data_path().download)

        insert_default_urls()
        urls = select_default_urls()
        files = os.listdir(data_path().download)

        # test file integrity
        for f in files:
            local_hash = filehash(data_path().download + f)
            found = False
            for u in urls:
                if u.fileName.strip() == f.strip() and u.sha_hash.strip() == local_hash.strip():
                    found = True
                    break
            if not found:
                os.remove(data_path().download + f)

        self.max_range = len(urls) * 2 + 1
        self.totalDownloads = len(urls) + 1
        self.currentDownload = 0
        for u in urls:
            self.download_file(u)
            self.value = math.floor(self.value)
            self.value += 1

        self.message = 'Updating gzdoom...'
        update = self.update_gz_doom()
        self.value += 1
        if not update:
            write_log('Update gzdoom failed', True)

        file_names = os.listdir(data_path().download)
        self.message = "Extracting/Copying files..."

        game_files = []
        for z in file_names:
            ext_pos = z.rfind(".")
            file_format = "zip"
            if ext_pos >= 0:
                file_format = z[ext_pos + 1:].lower()
            game_files.append(GameFile(z, file_format))

        for z in game_files:
            if z.test_file_name("blasphem"):
                z.extract_to(data_path().wad)
            elif z.test_file_name("freedoom"):
                z.extract_to(data_path().temp)
                temp_names = os.listdir(data_path().temp)
                for f in temp_names:
                    if f.lower().find("freedoom") >= 0:
                        temp_names2 = os.listdir(data_path().temp + f)
                        for g in temp_names2:
                            if g.lower().find("wad") >= 0:
                                h = data_path().temp + f + "/" + g
                                if not os.path.exists(data_path().wad):
                                    os.makedirs(data_path().wad)
                                shutil.copy(h, data_path().wad)
            elif z.test_file_name("pk3") or z.test_file_name("150skins"):
                z.copy_to(data_path().mod)
            elif z.test_file_name("harmonyc"):
                z.extract_to(data_path().temp)
                temp_names = os.listdir(data_path().temp)
                for f in temp_names:
                    if f.lower().find("harmonyc") >= 0:
                        shutil.copy(data_path().temp + f, data_path().wad)
                    if f.lower().find("extra") >= 0:
                        shutil.copy(data_path().temp + f + '/Harm-WS.wad', data_path().wad)
                z.extract_to(data_path().wad)
            elif z.test_file_name("cats"):  # space cats saga is a total conversion, can run as a game and as a mod
                z.extract_to(data_path().temp)
                temp_names = os.listdir(data_path().temp)
                for f in temp_names:
                    if f.lower().find("cats") >= 0:
                        temp_names2 = os.listdir(data_path().temp + f)
                        for g in temp_names2:
                            if g.lower().find("wad") >= 0:
                                h = data_path().temp + f + "/" + g
                                if not os.path.exists(data_path().mod):
                                    os.makedirs(data_path().mod)
                                shutil.copy(h, data_path().mod)

            elif not z.test_file_name("gzdoom") and not z.test_file_name("wine"):
                z.copy_to(data_path().map)
            self.value += 1

        if os.path.exists(data_path().temp):
            shutil.rmtree(data_path().temp)

        create_db()
        self.value += 1

        self.message = 'All done, have fun!'
        # self.value = self.max_range
        self.finish_task()

    def finish_task(self):
        self.done = True
        if self.clock:
            Clock.unschedule(self.clock.get_callback())
            Clock.schedule_once(self.clock.get_callback())

    def verify_update(self):
        self.done = False
        self.max_range = 1
        self.totalDownloads = 1
        self.message = 'Verifying GZDoom Version...'
        self.currentDownload = 1
        result = self.update_gz_doom()
        if result == 2:
            self.message = 'GZDoom already at latest version.'
        elif result:
            self.message = 'GZDoom updated to version: ' + read_config('gzdversion', 'text')
        else:
            self.message = 'Update failed!\nRead ' + data_path().logFile + ' for more details!'
        self.value = self.max_range
        self.finish_task()

    def update_gz_doom(self, gzdoom_update=None):
        result = False
        try:
            update_wine = False
            if os.name != "nt" and WINE_GZDOOM:
                wine_hash = filehash(data_path().wine)
                update_wine = (wine_hash !=
                               'a59afda035da121819589338507d1370a146052d7361bea074fc86dab86bce13')

            if gzdoom_update:
                finish = True
                self.max_range = 1
                self.totalDownloads = 1
            else:
                finish = False
                gzdoom_update = GZDoomUpdate()

            if update_wine:
                self.max_range += 1
                self.totalDownloads += 1

            if gzdoom_update.check_gzdoom_update():
                self.download_file(gzdoom_update.file)

                if gzdoom_update.gzdoom_windows:
                    zip_file = GameFile(gzdoom_update.filename, "zip")
                else:
                    zip_file = GameFile(gzdoom_update.filename, "xz")

                extract_ok = False
                if zip_file.test_file_name("gzdoom"):
                    try:
                        if gzdoom_update.gzdoom_windows:
                            if zip_file.extract_to(data_path().gzDoom):
                                extract_ok = True
                        else:
                            if zip_file.extract_to(data_path().temp):
                                extract_ok = True
                            dirs = os.listdir(data_path().temp)
                            for d in dirs:
                                if d.lower().find("gzdoom") >= 0:
                                    if os.path.exists(data_path().gzDoom):
                                        shutil.rmtree(data_path().gzDoom)
                                    shutil.copytree(data_path().temp + d, data_path().gzDoom)
                        gzdoom_update.local_hash = filehash(gzdoom_update.local_file_name)
                    except Exception as e:
                        write_log(e)

                    update_gzdoom_version(gzdoom_update.version, gzdoom_update.local_hash)
                    if os.path.exists(data_path().temp):
                        shutil.rmtree(data_path().temp)

                result = extract_ok and (os.path.isfile(gzdoom_update.local_file_name))

                if update_wine:
                    url = Url("https://github.com/GloriousEggroll/wine-ge-custom/releases"
                              "/download/GE-Proton8-26/wine-lutris-GE-Proton8-26-x86_64.tar.xz",
                              "wine.tar.xz")
                    self.value = math.floor(self.value)
                    self.value += 1
                    self.download_file(url)
                    self.message = "Extracting wine..."
                    zip_file = GameFile('wine.tar.xz', 'xz')
                    zip_file.extract_to(data_path().gzDoom)
            else:
                result = 2

            if finish:
                self.message = self.message = 'GZDoom updated to version: ' + read_config('gzdversion', 'text')
                self.finish_task()
        except Exception as e:
            write_log(e)

        return result

    def download_file(self, url):
        if not os.path.isfile(url.get_file_path()):
            url.on_progress = self.url_on_progress
            url.on_failure = self.url_on_failure
            url.download()

        self.currentDownload += 1

    def url_on_progress(self, _request, current_size, total_size):
        # updates dialog based on a fixed max range since I don't know the total size of all files before download
        # each file.
        if current_size < total_size:
            self.value = math.floor(self.value) + (current_size / total_size)
        self.message = "Downloading file " + str(self.currentDownload) \
                       + "/" + str(self.totalDownloads) + ": " \
                       + str(current_size // 1024) + "k of " + str(total_size // 1024) + "k"

    @staticmethod
    def url_on_failure(request, result):
        log(str(request) + ': ' + str(result))


class GameFile:
    _format = ""
    _name = ""

    def __init__(self, name, file_format="z"):
        self._format = file_format
        self._name = name

    def extract_to(self, path):
        from_file = data_path().download + self._name
        if not os.path.exists(path):
            os.mkdir(path)
        if os.path.isfile(from_file):
            try:
                if self.get_format() == "zip":
                    z = ZipFile(from_file)
                    z.extractall(path)

                if self.get_format() == "xz":
                    z = TarFile(from_file, 'r:xz')
                    z.extractall(path)

                if self.get_format() == "7z":
                    z = SevenZipFile(from_file, 'r')
                    z.extractall(path)
                return True
            except Exception as e:
                write_log("ExtractTo - " + str(e))
        else:
            write_log("File: " + from_file + " not found!")
        return False

    def copy_to(self, path):
        try:
            from_file = data_path().download + self._name

            if self.get_format() == "zip" or self.get_format() == "pk3":
                z = ZipFile(from_file)
                z.testzip()

            if not os.path.exists(path):
                os.mkdir(path)

            if os.path.isfile(from_file):
                shutil.copy(from_file, path)
        except Exception as e:
            write_log("CopyTo - " + str(e))
            write_log("Copying " + self.get_name() + " failed")

    def get_name(self):
        return self._name

    def test_file_name(self, f_name):
        if self.get_name().lower().find(f_name) >= 0:
            return True
        else:
            return False

    def get_format(self):
        return self._format

    def get_map_name(self):
        from_file = data_path().download + self.get_name()
        z = ZipFile(from_file)

        # Mps with non-standard txt
        if self.get_name() == "mm2.zip":
            return "Memento Mori 2"
        if self.get_name() == "av.zip":
            return "Alien Vendetta"
        if self.get_name() == "hr.zip":
            return "Hell Revealed"

        try:
            txt_file = z.namelist()
            for t in txt_file:
                if t.lower().find(".txt") >= 0:
                    with z.open(t) as f:
                        names = f.readlines()
                        for name in names:
                            s = str(name)
                            if (s.find("Title ") == 2) and (s.find(":") >= 0) and (s.find("Screen") < 0):
                                start = s.find(":") + 1
                                s = s.replace("\\n", "")
                                s = s.replace("\\r", "")
                                s = s.replace("'", "")
                                s = s.replace(".wad", "")
                                return s[start:].strip()
        except Exception as e:
            write_log("GetMapName - " + str(e))
            return self.get_name()
        return self.get_name()
