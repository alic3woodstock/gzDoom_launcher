import os
import shutil
import zipfile
import wx
import tarfile
import gameDefDb
import gameDef
import wx.lib.dialogs as wxdialogs
import functions
import download


class ZipFile:
    _format = ""
    _name = ""

    def __init__(self, name, fileFormat="z"):
        self._format = fileFormat
        self._name = name

    def ExtractTo(self, path):
        fromFile = functions.downloadPath + self._name
        if not os.path.exists(path):
            os.mkdir(path)
        if os.path.isfile(fromFile):
            try:
                if self.GetFormat() == "zip":
                    z = zipfile.ZipFile(fromFile)
                    z.extractall(path)

                if self.GetFormat() == "xz":
                    z = tarfile.open(fromFile, 'r:xz')
                    z.extractall(path)

                return True
            except Exception as e:
                functions.log("ExtractTo - " + str(e))
                print("Extracting " + self.GetName() + " failed")
        return False

    def CopyTo(self, path):
        try:
            fromFile = functions.downloadPath + self._name

            if self.GetFormat() == "zip" or self.GetFormat() == "pk3":
                z = zipfile.ZipFile(fromFile)
                z.testzip()

            if not os.path.exists(path):
                os.mkdir(path)

            if os.path.isfile(fromFile):
                shutil.copy(fromFile, path)
        except Exception as e:
            functions.log("CopyTo - " + str(e))
            functions.log("Copying " + self.GetName() + " failed")

    def GetName(self):
        return self._name

    def TestFileName(self, fName):
        if self.GetName().lower().find(fName) >= 0:
            return True
        else:
            return False

    def GetFormat(self):
        return self._format

    def GetMapName(self):
        fromFile = functions.downloadPath + self.GetName()
        z = zipfile.ZipFile(fromFile)

        # Mps with non-standard txt
        if self.GetName() == "mm2.zip":
            return "Memento Mori 2"
        if self.GetName() == "av.zip":
            return "Alien Vendetta"
        if self.GetName() == "hr.zip":
            return "Hell Revealed"

        try:
            txtFile = z.namelist()
            for t in txtFile:
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
            return self.GetName()
        return self.GetName()


def ExtractAll(parent):
    progress = wx.ProgressDialog("Extract and Create Database", "Extracting/Copying files...", download.MAX_RANGE,
                                 parent=parent, style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)

    download.StartDownload(parent, False, progress)
    download.UpdateGzDoom(parent, False, progress)
    fileNames = os.listdir(functions.downloadPath)
    progress.SetRange(len(fileNames) * 2)
    progress.Update(0, "Extracting/Copying files...")

    zipFiles = []
    for z in fileNames:
        extPos = z.rfind(".")
        fileFormat = "zip"
        if extPos >= 0:
            fileFormat = z[extPos + 1:].lower()
        zipFiles.append(ZipFile(z, fileFormat))

    progress.SetRange(len(zipFiles) + 22)  # if everthyng works number of csv in the list is 22
    i = 1
    for z in zipFiles:
        if z.TestFileName("blasphem"):
            z.ExtractTo(functions.wadPath)
        elif z.TestFileName("freedoom"):
            z.ExtractTo(functions.tempDir)
            tempNames = os.listdir(functions.tempDir)
            for f in tempNames:
                if f.lower().find("freedoom") >= 0:
                    tempNames2 = os.listdir(functions.tempDir + f)
                    for g in tempNames2:
                        if g.lower().find("wad") >= 0:
                            h = functions.tempDir + f + "/" + g
                            if not os.path.exists(functions.wadPath):
                                os.makedirs(functions.wadPath)
                            shutil.copy(h, functions.wadPath)
        elif z.TestFileName("pk3") or z.TestFileName("150skins"):
            z.CopyTo(functions.modPath)
        elif not z.TestFileName("gzdoom"):
            z.CopyTo(functions.mapPath)
        progress.Update(i)
        i += 1

    # Remove temp directory if exists
    if os.path.exists(functions.tempDir):
        shutil.rmtree(functions.tempDir)

    CreateDB(progress)


def CreateDB(progress):
    dbGames = gameDefDb.GameDefDb()
    dbGames.DeleteGameTable()
    dbGames.CreateGameTable()

    zipFiles = []
    games = []

    wads = os.listdir(functions.wadPath)
    for w in wads:
        zipFiles.append(ZipFile(w, functions.wadPath))  # store path in format string since I don't need to use Extract

    maps = os.listdir(functions.mapPath)
    for a in maps:
        zipFiles.append(ZipFile(a, functions.mapPath))

    mods = os.listdir(functions.modPath)
    for m in mods:
        zipFiles.append(ZipFile(m, functions.modPath))

    blasphemWad = ""

    gameExec = functions.gzDoomExec

    i = 0
    for z in zipFiles:
        try:
            fullPath = z.GetFormat() + z.GetName()
            if z.TestFileName("blasphem"):
                blasphemWad = fullPath  # works because wad comes first in the list
            elif z.TestFileName("bls"):
                games.append(gameDef.GameDef(i, "Blasphem", 0, gameExec, 2, 0, blasphemWad, [fullPath]))
            elif z.TestFileName("freedoom1"):
                games.append(gameDef.GameDef(i, "Freedoom Phase 1", 0, gameExec, 1, 0, fullPath))
            elif z.TestFileName("freedoom2"):
                games.append(gameDef.GameDef(i, "Freedoom Phase 2", 0, gameExec, 1, 0, fullPath))
            elif z.GetFormat().find("maps") >= 0:
                if z.TestFileName("htchest") or z.TestFileName("unbeliev"):
                    games.append(gameDef.GameDef(i, z.GetMapName(), 1, gameExec, 2, 0,
                                                 functions.wadPath + "blasphem-0.1.7.wad", [functions.wadPath + "BLSMPTXT.WAD", fullPath]))
                else:
                    games.append(gameDef.GameDef(i, z.GetMapName(), 1, gameExec, 1, 0,
                                                 functions.wadPath + "freedoom2.wad", [fullPath]))
            elif z.GetFormat().find("mods") >= 0:
                if z.TestFileName("150skins"):
                    games.append(gameDef.GameDef(i, "150 Skins", -1, gameExec, 2, 0,  # 150 Skins also works with heretic
                                                 "", [fullPath]))
                elif z.TestFileName("beautiful"):
                    games.append(gameDef.GameDef(i, "Beautiful Doom", -1, gameExec, 1, 0,
                                                 "", [functions.modPath + "150skins.zip", fullPath]))
                elif z.TestFileName("brutal"):
                    games.append(gameDef.GameDef(i, "Brutal Doom", -1, gameExec, 1, 0,
                                                 "", [fullPath]))
        except Exception as e:
            functions.log("CreateDB - " + str(e))
        i += 1

    done = i + 21
    progress.SetRange(done + len(games))
    for g in games:
        if progress.GetRange() < done:
            progress.SetRange(done)
        progress.Update(done, "Creating games database...")
        dbGames.InsertGame(g)
        done += 1

    progress.Destroy()
    wxdialogs.messageDialog(message="Database creation done, have fun!",
                            title='Reset to default games', aStyle=wx.ICON_INFORMATION | wx.OK | wx.RIGHT)
