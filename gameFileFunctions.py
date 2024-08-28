import math
import os
import shutil
import stat
from tarfile import open as TarFile
from zipfile import ZipFile

import requests
from kivy.clock import Clock
from py7zr import SevenZipFile

import functions
from createDB import CreateDB
from gameDef import GameDef
from gameDefDB import delete_game_table, insert_game
from url import Url
from urlDB import insert_default_urls, select_default_urls, get_moddb_url


def get_gz_doom_url(gzdoom_windows):
    r = requests.get("https://github.com/coelckers/gzdoom/releases/latest", stream=False)

    tmp_str = r.text
    start = tmp_str.find("https://github.com/ZDoom/gzdoom/releases/expanded_assets")
    end = tmp_str.find('"', start)
    tmp_str = tmp_str[start:end].strip()
    start = tmp_str.find("expanded_assets/g")
    version = tmp_str[start:].strip()
    version = version[version.find('g') + 1:]

    r = requests.get(tmp_str)
    tmp_str = r.text

    start = tmp_str.find("/ZDoom/gzdoom/releases/download")
    tmp_str = tmp_str[start:]
    if gzdoom_windows:
        start = tmp_str.lower().find('windows.zip')
    else:
        start = tmp_str.lower().find('linux')
    start = tmp_str.find("/ZDoom/gzdoom/releases/download", start - 200, )
    tmp_str = tmp_str[start:]
    end = tmp_str.lower().find('" rel=')

    tmp_str = "https://github.com" + tmp_str[:end].strip()
    functions.log(tmp_str, False)
    return [tmp_str, version]


def create_db():
    db_games = CreateDB()
    delete_game_table()
    db_games.create_game_table()

    game_files = []
    games = []

    wads = os.listdir(functions.wadPath)
    for w in wads:
        game_files.append(
            GameFile(w, functions.wadPath))  # store path in format string since I don't need to use Extract

    maps = os.listdir(functions.mapPath)
    for a in maps:
        game_files.append(GameFile(a, functions.mapPath))

    mods = os.listdir(functions.modPath)
    for m in mods:
        game_files.append(GameFile(m, functions.modPath))

    blasphem_wad = ""
    blasphem_texture = ""

    game_exec = functions.gzDoomExec

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
                                         functions.wadPath + "blasphem.wad",
                                         [functions.wadPath + "BLSMPTXT.WAD", full_path]))
                else:
                    games.append(GameDef(i, z.get_map_name(), 1, game_exec, 1, 0,
                                         functions.wadPath + "freedoom2.wad", [full_path]))
            elif z.get_format().find("mods") >= 0:
                if z.test_file_name("150skins"):
                    games.append(
                        GameDef(i, "150 Skins", -1, game_exec, 2, 0,  # 150 Skins also works with heretic
                                "", [full_path]))
                    games.append(
                        GameDef(i, "150 Skins", -1, game_exec, 1, 0,  # 150 Skins also works with heretic
                                "", [full_path]))
                elif z.test_file_name("beautiful"):
                    games.append(GameDef(i, "Beautiful Doom", -1, game_exec, 1, 0,
                                         "", [functions.modPath + "150skins.zip", full_path]))
                elif z.test_file_name("brutal"):
                    games.append(GameDef(i, "Brutal Doom", -1, game_exec, 1, 0,
                                         "", [full_path]))
                elif z.test_file_name("evp") and z.test_file_name("pk3"):
                    games.append(GameDef(i, "Enhanced Vanilla Project", -1, game_exec, 1, 0,
                                         "", [functions.modPath + "150skins.zip", full_path]))
                elif z.test_file_name("cats"):
                    games.append(GameDef(i, "Space Cats Saga", 0, game_exec, 5, 0,
                                         functions.wadPath + "freedoom2.wad", [full_path]))
                    i += 1
                    games.append(GameDef(i, "Space Cats Saga", -1, game_exec, 1, 0,
                                         "", [full_path]))

            if blasphem_wad.strip() and blasphem_texture.strip():  # insert game only if both files are ok
                games.append(GameDef(i, "Blasphem", 0, game_exec, 2, 0, blasphem_wad, [blasphem_texture]))
                blasphem_wad = ""
                blasphem_texture = ""

        except Exception as e:
            functions.log("CreateDB - " + str(e))

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

        if functions.RE_DOWNLOAD:
            shutil.rmtree(functions.downloadPath)

        if not os.path.exists(functions.downloadPath):
            os.mkdir(functions.downloadPath)

        insert_default_urls()
        urls = select_default_urls()
        files = os.listdir(functions.downloadPath)

        # test file integrity
        for f in files:
            local_hash = functions.filehash(functions.downloadPath + f)
            found = False
            for u in urls:
                if u.fileName.strip() == f.strip() and u.sha_hash.strip() == local_hash.strip():
                    found = True
                    break
            if not found:
                os.remove(functions.downloadPath + f)

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
            functions.log('Update gzdoom failed', True)

        file_names = os.listdir(functions.downloadPath)
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
                z.extract_to(functions.wadPath)
            elif z.test_file_name("freedoom"):
                z.extract_to(functions.tempDir)
                temp_names = os.listdir(functions.tempDir)
                for f in temp_names:
                    if f.lower().find("freedoom") >= 0:
                        temp_names2 = os.listdir(functions.tempDir + f)
                        for g in temp_names2:
                            if g.lower().find("wad") >= 0:
                                h = functions.tempDir + f + "/" + g
                                if not os.path.exists(functions.wadPath):
                                    os.makedirs(functions.wadPath)
                                shutil.copy(h, functions.wadPath)
            elif z.test_file_name("pk3") or z.test_file_name("150skins"):
                z.copy_to(functions.modPath)
            elif z.test_file_name("harmonyc"):
                z.extract_to(functions.tempDir)
                temp_names = os.listdir(functions.tempDir)
                for f in temp_names:
                    if f.lower().find("harmonyc") >= 0:
                        shutil.copy(functions.tempDir + f, functions.wadPath)
                    if f.lower().find("extra") >= 0:
                        shutil.copy(functions.tempDir + f + '/Harm-WS.wad', functions.wadPath)
                z.extract_to(functions.wadPath)
            elif z.test_file_name("cats"):  # space cats saga is a total conversion, can run as a game and as a mod
                z.extract_to(functions.tempDir)
                temp_names = os.listdir(functions.tempDir)
                for f in temp_names:
                    if f.lower().find("cats") >= 0:
                        temp_names2 = os.listdir(functions.tempDir + f)
                        for g in temp_names2:
                            if g.lower().find("wad") >= 0:
                                h = functions.tempDir + f + "/" + g
                                if not os.path.exists(functions.modPath):
                                    os.makedirs(functions.modPath)
                                shutil.copy(h, functions.modPath)

            elif not z.test_file_name("gzdoom") and not z.test_file_name("wine"):
                z.copy_to(functions.mapPath)
            self.value += 1

        if os.path.exists(functions.tempDir):
            shutil.rmtree(functions.tempDir)

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

    def download_file(self, url):
        # updates dialog based on a fixed max range since I don't know the total size of all files before download
        # each file.
        if url.url.find("moddb") >= 0:
            url.url = get_moddb_url(url.url)
        if not os.path.isfile(url.GetFilePath()):
            r = requests.get(url.url, stream=True)
            with open(url.GetFilePath(), "wb") as downloadF:
                total_length = r.headers.get('content-length')
                if total_length is None:
                    total_length = 0
                else:
                    total_length = int(total_length)
                i = 1024

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        if total_length > 0:
                            # Adding 1 prevents dialog freezes even with download completed
                            str_total = str(total_length // 1024)
                        else:
                            str_total = "..."
                        downloadF.write(chunk)
                    if i < total_length:
                        self.value = math.floor(self.value) + (i / total_length)

                    i += 1024

                    self.message = "Downloading file " + str(self.currentDownload) \
                                   + "/" + str(self.totalDownloads) + ": " \
                                   + str(i // 1024) + "k of " + str_total + "k"

        self.currentDownload += 1

    def verify_update(self):
        self.done = False
        if os.name != "nt" and functions.WINE_GZDOOM:
            self.max_range = 2
            self.totalDownloads = 2
        else:
            self.max_range = 1
            self.totalDownloads = 1
        self.message = 'Verifying GZDoom Version...'
        self.currentDownload = 1
        result = self.update_gz_doom()
        if result == 2:
            self.message = 'GZDoom already at latest version.'
        elif result:
            data_con = CreateDB()
            self.message = 'GZDoom updated to version: ' + data_con.ReadConfig('gzdversion', 'text')
        else:
            self.message = 'Update failed!\nRead ' + functions.logFile + ' for more details!'
        self.value = self.max_range
        self.finish_task()

    def update_gz_doom(self):
        if not os.path.exists(functions.downloadPath):
            os.mkdir(functions.downloadPath)

        gzdoom_windows = (os.name == "nt") or functions.WINE_GZDOOM
        wine_gzdoom = not (os.name == "nt") and functions.WINE_GZDOOM

        if gzdoom_windows:
            filename = "gzdoom.zip"
        else:
            filename = "gzdoom.tar.xz"

        if wine_gzdoom:
            local_file_name = functions.gzDoomExec + ".exe"
        else:
            local_file_name = functions.gzDoomExec

        if os.path.exists(functions.downloadPath + filename):
            os.remove(functions.downloadPath + filename)

        if os.path.exists(functions.downloadPath + 'wine.tar.xz'):
            os.remove(functions.downloadPath + 'wine.tar.xz')

        result = False
        try:
            gzdoom_url = get_gz_doom_url(gzdoom_windows)
            url = gzdoom_url[0]
            version = gzdoom_url[1]
            file = Url(url, filename)
            game_data = CreateDB()
            local_hash = functions.filehash(local_file_name)

            if (not os.path.isfile(local_file_name)) or (not game_data.CheckGzDoomVersion(version, local_hash)):
                self.download_file(file)

                if gzdoom_windows:
                    zip_file = GameFile(filename, "zip")
                else:
                    zip_file = GameFile(filename, "xz")

                extract_ok = False
                if zip_file.test_file_name("gzdoom"):
                    try:
                        if gzdoom_windows:
                            if zip_file.extract_to(functions.gzDoomPath):
                                extract_ok = True
                        else:
                            if zip_file.extract_to(functions.tempDir):
                                extract_ok = True
                            dirs = os.listdir(functions.tempDir)
                            for d in dirs:
                                if d.lower().find("gzdoom") >= 0:
                                    if os.path.exists(functions.gzDoomPath):
                                        shutil.rmtree(functions.gzDoomPath)
                                    shutil.copytree(functions.tempDir + d, functions.gzDoomPath)
                        local_hash = functions.filehash(local_file_name)
                    except Exception as e:
                        functions.log(e)

                    game_data.UpdateGzdoomVersion(version, local_hash)
                    if os.path.exists(functions.tempDir):
                        shutil.rmtree(functions.tempDir)

                result = extract_ok and (os.path.isfile(local_file_name))

                if wine_gzdoom:
                    url = Url("https://github.com/GloriousEggroll/wine-ge-custom/releases"
                              "/download/GE-Proton8-26/wine-lutris-GE-Proton8-26-x86_64.tar.xz",
                              "wine.tar.xz")
                    self.value = math.floor(self.value)
                    self.value += 1
                    self.download_file(url)
                    self.message = "Extracting wine..."
                    zip_file = GameFile('wine.tar.xz', 'xz')
                    zip_file.extract_to(functions.gzDoomPath)
                    tmp_params = ""
                    for i in range(1, 20):
                        tmp_params += ' "$' + str(i) + '" '
                    wine_cmd = ('WINEPREFIX=' + functions.dataPath + '/.wine '
                                + functions.gzDoomPath + 'lutris-GE-Proton8-26-x86_64/bin/wine64 '
                                + local_file_name + tmp_params)
                    file = open(functions.gzDoomExec, 'wt')
                    file.writelines(['#!/bin/bash\n',
                                     wine_cmd])
                    file.close()
                    os.chmod(functions.gzDoomExec, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
            else:
                result = 2
        except Exception as e:
            functions.log(e)

        return result


class GameFile:
    _format = ""
    _name = ""

    def __init__(self, name, file_format="z"):
        self._format = file_format
        self._name = name

    def extract_to(self, path):
        from_file = functions.downloadPath + self._name
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
                functions.log("ExtractTo - " + str(e))
        else:
            functions.log("File: " + from_file + " not found!")
        return False

    def copy_to(self, path):
        try:
            from_file = functions.downloadPath + self._name

            if self.get_format() == "zip" or self.get_format() == "pk3":
                z = ZipFile(from_file)
                z.testzip()

            if not os.path.exists(path):
                os.mkdir(path)

            if os.path.isfile(from_file):
                shutil.copy(from_file, path)
        except Exception as e:
            functions.log("CopyTo - " + str(e))
            functions.log("Copying " + self.get_name() + " failed")

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
        from_file = functions.downloadPath + self.get_name()
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
            functions.log("GetMapName - " + str(e))
            return self.get_name()
        return self.get_name()
