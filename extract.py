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
        fromFile = "downloads/" + self._name
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
                functions.log(e)
                print("Extracting " + self.GetName() + " failed")
        return False

    def CopyTo(self, path):
        try:
            fromFile = "downloads/" + self._name

            if (self.GetFormat() == "zip") or (self.GetFormat() == "pk3"):
                z = zipfile.ZipFile(fromFile)
                z.testzip

            if not os.path.exists(path):
                os.mkdir(path)

            if os.path.isfile(fromFile):
                shutil.copy(fromFile, path)
        except Exception as e:
            functions.log(e)
            print("Copying " + self.GetName() + " failed")

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
        fromFile = "downloads/" + self.GetName()
        z = zipfile.ZipFile(fromFile)

        # Mps with non standard txt
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
        except:
            return self.GetName()
        return self.GetName()


def ExtractAll(parent):
    progress = wx.ProgressDialog("Extract and Create Database", "Extracting/Copying files...", maximum=100,
                                 parent=parent, style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)

    fileNames = os.listdir("downloads")
    progress.SetRange(len(fileNames) * 2)
    download.StartDownload(parent, False)

    zipFiles = []
    for z in fileNames:
        extPos = z.rfind(".")
        fileFormat = "zip"
        if extPos >= 0:
            fileFormat = z[extPos + 1:].lower()
        zipFiles.append(ZipFile(z, fileFormat))

    progress.SetRange(len(zipFiles) + 22)  # if everthyng works number of csv in the list is 22
    i = 1;
    for z in zipFiles:
        if z.TestFileName("gzdoom"):
            if os.name == "nt":
                z.ExtractTo("gzdoom")
            else:
                try:
                    z.ExtractTo("temp")
                    dirs = os.listdir("temp")
                    for dir in dirs:
                        if dir.lower().find("gzdoom") >= 0:
                            if os.path.exists("gzdoom"):
                                shutil.rmtree("gzdoom")
                            shutil.copytree("temp/" + dir, "gzdoom")
                except Exception as e:
                    functions.log(e)
                    print("Copying gzdoom failed!")
        elif z.TestFileName("blasphem"):
            z.ExtractTo("wads")
        elif z.TestFileName("freedoom"):
            z.ExtractTo("temp")
            tempNames = os.listdir("temp")
            for f in tempNames:
                if f.lower().find("freedoom") >= 0:
                    tempNames2 = os.listdir("temp/" + f)
                    for g in tempNames2:
                        if g.lower().find("wad") >= 0:
                            h = "temp/" + f + "/" + g
                            if not os.path.exists("wads"):
                                os.mkdir("wads")
                            shutil.copy(h, "wads")
        elif z.TestFileName("pk3") or z.TestFileName("150skins"):
            z.CopyTo("mods")
        else:
            z.CopyTo("maps")
        progress.Update(i)
        i += 1

    # Remove temp directory if exists
    if os.path.exists("temp"):
        shutil.rmtree("temp")

    CreateDB(progress)


def CreateDB(progress):
    dbGames = gameDefDb.GameDefDb()
    dbGames.DeleteGameTable()
    dbGames.CreateGameTable()

    zipFiles = []
    games = []

    wads = os.listdir("wads")
    for w in wads:
        zipFiles.append(ZipFile(w, "wads"))  # store path in format string since I don't need to use Extract

    maps = os.listdir("maps")
    for a in maps:
        zipFiles.append(ZipFile(a, "maps"))

    mods = os.listdir("mods")
    for m in mods:
        zipFiles.append(ZipFile(m, "mods"))

    blasphemWad = ""

    if os.name == "nt":
        gameExec = ".\\gzdoom\\gzdoom.exe"
    else:
        gameExec = "./gzdoom/gzdoom"

    i = 0
    for z in zipFiles:
        fullPath = z.GetFormat() + "/" + z.GetName()
        if z.TestFileName("blasphem"):
            blasphemWad = (fullPath)  # works because wad comes first in the list
        elif z.TestFileName("bls"):
            games.append(gameDef.GameDef(i, "Blasphem", 0, gameExec, 2, 0, blasphemWad, [fullPath]))
        elif z.TestFileName("freedoom1"):
            games.append(gameDef.GameDef(i, "Freedoom Phase 1", 0, gameExec, 1, 0, fullPath))
        elif z.TestFileName("freedoom2"):
            games.append(gameDef.GameDef(i, "Freedoom Phase 2", 0, gameExec, 1, 0, fullPath))
        elif z.GetFormat() == "maps":
            if z.TestFileName("htchest") or z.TestFileName("unbeliev"):
                games.append(gameDef.GameDef(i, z.GetMapName(), 1, gameExec, 2, 0,
                                             "wads/blasphem-0.1.7.wad", ["wads/BLSMPTXT.WAD", fullPath]))
            else:
                games.append(gameDef.GameDef(i, z.GetMapName(), 1, gameExec, 1, 0,
                                             "wads/freedoom2.wad", [fullPath]))
        elif z.GetFormat() == "mods":
            if z.TestFileName("150skins"):
                games.append(gameDef.GameDef(i, "150 Skins", -1, gameExec, 2, 0,  # 150 Skins also works with heretic
                                             "", ["mods/150skins.zip"]))
            elif z.TestFileName("beaultiful"):
                games.append(gameDef.GameDef(i, "Beautiful Doom", -1, gameExec, 1, 0,
                                             "", ["mods/150skins.zip", "mods/Beautiful_Doom.pk3"]))
            elif z.TestFileName("brutal"):
                games.append(gameDef.GameDef(i, "Brutal Doom", -1, gameExec, 1, 0,
                                             "", ["mods/brutal.pk3"]))
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
