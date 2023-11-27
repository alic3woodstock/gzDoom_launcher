import wx
import requests
import os
import wx.lib.dialogs as wxdialogs
import functions
import extract
import shutil
import gameDefDb

# class MyDialog(wx.Dialog): 
# def __init__(self, parent, title):
# super(MyDialog, self).__init__(parent, title = title, size = (250,150))
# panel = wx.Panel(self)
# self.btn = wx.Button(panel, wx.ID_OK, label = "ok", size = (50,20), pos = (75,50))

MAX_RANGE = 1000
totalFiles = 0
current = 0


class Url:
    _url = ""
    _fileName = ""

    def __init__(self, url, fileName):
        self._url = url
        self._fileName = fileName

    def GetUrl(self):
        return self._url

    def GetFileName(self):
        return self._fileName

    def GetFilePath(self):
        return functions.downloadPath + self._fileName


def StartDownload(parent, showmessage=True, progress=None):
    if not progress:
        progress = ShowProgress(parent)

    if not os.path.exists(functions.downloadPath):
        os.mkdir(functions.downloadPath)

    files = [
        # Blasphemer
        Url("https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphem-0.1.7.zip", "blasphem.zip"),
        Url("https://github.com/Blasphemer/blasphemer/releases/download/v0.1.7/blasphemer-texture-pack.zip",
            "blasphemer-texture-pack.zip"),

        # Freedoom
        Url("https://github.com/freedoom/freedoom/releases/download/v0.12.1/freedoom-0.12.1.zip", "freedoom.zip"),

        # 150skins
        Url("https://awxdeveloper.edu.eu.org/downloads/150skins.zip", "150skins.zip"), #my personal wordpress site

        # Beautiful Doom
        Url("https://github.com/jekyllgrim/Beautiful-Doom/releases/download/7.1.6/Beautiful_Doom_716.pk3",
            "Beautiful_Doom.pk3"),

        # Brutal Doom
        Url("https://github.com/BLOODWOLF333/Brutal-Doom-Community-Expansion/releases/download/V21.11.2/brutalv21.11"
            ".2.pk3",
            "brutal.pk3"), Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/av.zip", "av.zip"),

        # maps
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/aaliens.zip", "aliens.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e1.zip", "btsx_e1.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/btsx_e2.zip", "btsx_e2.zip"),
        Url("https://www.dropbox.com/s/vi47z1a4e4c4980/Sunder%202407.zip?dl=1", "sunder.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/eviternity.zip", "eviternity.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/gd.zip", "gd.zip"),
        Url("https://youfailit.net/pub/idgames/themes/hr/hr.zip", "hr.zip"),
        Url("https://youfailit.net/pub/idgames/themes/hr/hr2final.zip", "hr2final.zip"),
        Url("https://youfailit.net/pub/idgames/levels/heretic/Ports/htchest.zip", "htchest.zip"),
        Url("https://youfailit.net/pub/idgames/themes/mm/mm_allup.zip", "mm_allup.zip"),
        Url("https://youfailit.net/pub/idgames/themes/mm/mm2.zip", "mm2.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/pl2.zip", "pl2.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/megawads/scythe.zip", "scythe.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/scythe2.zip", "scythe2.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/s-u/scythex.zip", "scythex.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/sunlust.zip", "sunlust.zip"),
        Url("https://youfailit.net/pub/idgames/levels/heretic/s-u/unbeliev.zip", "unbeliev.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/valiant.zip", "valiant.zip"),
        Url("https://youfailit.net/pub/idgames/levels/doom2/Ports/megawads/zof.zip", "zof.zip")]

    global totalFiles
    totalFiles = len(files) + 1  # gzdoom will be downloaded by another function

    for f in files:
        try:
            GetFile(f, progress, showmessage)
        except Exception as e:
            functions.log(e)
            progress.Update(MAX_RANGE, "Failed to download " + f.GetFileName())


def GetFile(f, progress, showmessage=True):
    global current
    if current < totalFiles:
        current += 1

        # updates dialog based on a fixed max range since I don't know the total size of all files before download
        # each file.
        totalParc = (MAX_RANGE / totalFiles)
        percentDone = (current - 1) * totalParc

        if not os.path.isfile(f.GetFilePath()):
            r = requests.get(f.GetUrl(), stream=True)
            with open(f.GetFilePath(), "wb") as downloadF:
                total_length = r.headers.get('content-length')
                if total_length is None:
                    total_length = 0
                else:
                    total_length = int(total_length)
                i = 1024

                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        intProgress = int(round(percentDone))
                        if total_length > 0:
                            # Adding 1 prevents dialog freezes even with download completed
                            intProgress = int(round(i * totalParc / total_length + 1 + percentDone))
                            strTotal = str(total_length // 1024)
                        else:
                            strTotal = "..."
                        downloadF.write(chunk)
                    i += 1024

                    if intProgress >= MAX_RANGE:
                        intProgress = MAX_RANGE - 1

                    progress.Update(intProgress, "Downloading file " + str(current) + "/" + str(totalFiles) + ": " +
                                    str(i // 1024) + "k of " + strTotal + "k")
        else:
            intProgress = int(round(percentDone + totalParc))

            if intProgress >= MAX_RANGE:
                intProgress = MAX_RANGE - 1

            progress.Update(intProgress, "File exists, skiping...")

        if current == totalFiles:
            if showmessage:
                progress.Destroy()
                wxdialogs.messageDialog(message="Download complete!",
                                        title='Reset to default games', aStyle=wx.ICON_INFORMATION | wx.OK | wx.RIGHT)


def GetGzDoomUrl():
    r = requests.get("https://github.com/coelckers/gzdoom/releases/latest", stream=False)

    tmpStr = r.text
    start = tmpStr.find("https://github.com/ZDoom/gzdoom/releases/expanded_assets")
    end = tmpStr.find('"', start)
    tmpStr = tmpStr[start:end].strip()
    start = tmpStr.find("expanded_assets/g")
    version = tmpStr[start:].strip()
    version = version[version.find('g') + 1:]

    r = requests.get(tmpStr)
    tmpStr = r.text

    start = tmpStr.find("/ZDoom/gzdoom/releases/download")
    tmpStr = tmpStr[start:]
    if os.name == "nt":
        start = tmpStr.lower().find('windows-64bit.zip')
    else:
        start = tmpStr.lower().find('linux')
    start = tmpStr.find("/ZDoom/gzdoom/releases/download", start - 200, )
    tmpStr = tmpStr[start:]
    end = tmpStr.lower().find(' rel=')
    print(tmpStr[:end])

    tmpStr = "https://github.com" + tmpStr[:end].strip()
    functions.log(tmpStr, False)
    return [tmpStr, version]


def ShowProgress(parent):
    progress = wx.ProgressDialog("Download Files", "Starting Download...", maximum=100, parent=parent,
                                 style=wx.PD_APP_MODAL | wx.STAY_ON_TOP)
    progress.SetRange(MAX_RANGE)
    return progress


def UpdateGzDoom(parent, showMessage=True, progress=None):
    if not progress:
        progress = ShowProgress(parent)

    global totalFiles
    if not os.path.exists(functions.downloadPath):
        os.mkdir(functions.downloadPath)

    if os.name == "nt":
        filename = "gzdoom.zip"
    else:
        filename = "gzdoom.tar.xz"

    localFileName = functions.gzDoomExec

    if os.path.exists(functions.downloadPath + filename):
        os.remove(functions.downloadPath + filename)

    if showMessage:
        totalFiles = 1
    gzdoomUrl = GetGzDoomUrl()
    url = gzdoomUrl[0]
    version = gzdoomUrl[1]
    print(gzdoomUrl)
    file = Url(url, filename)
    gameData = gameDefDb.GameDefDb()
    localHash = functions.filehash(localFileName)

    if (not os.path.isfile(localFileName)) or (not gameData.CheckGzDoomVersion(version, localHash)):
        GetFile(file, progress, False)

        if os.name == "nt":
            zipfile = extract.ZipFile(filename, "zip")
        else:
            zipfile = extract.ZipFile(filename, "xz")

        extractOK = False
        if zipfile.TestFileName("gzdoom"):
            if os.name == "nt":
                if zipfile.ExtractTo(functions.gzDoomPath):
                    extractOK = True
            else:
                try:
                    if zipfile.ExtractTo(functions.tempDir):
                        extractOK = True
                    dirs = os.listdir(functions.tempDir)
                    for d in dirs:
                        if d.lower().find("gzdoom") >= 0:
                            if os.path.exists(functions.gzDoomPath):
                                shutil.rmtree(functions.gzDoomPath)
                            shutil.copytree(functions.tempDir + d, functions.gzDoomPath)
                    localHash = functions.filehash(localFileName)
                    if showMessage:
                        progress.Destroy()
                except Exception as e:
                    functions.log(e)
            gameData.UpdateGzdoomVersion(version, localHash)
            if os.path.exists(functions.tempDir):
                shutil.rmtree(functions.tempDir)
        if showMessage:
            if extractOK and (os.path.isfile(functions.gzDoomExec) or os.path.isfile(functions.gzDoomExec)):
                wxdialogs.messageDialog(parent, "Gzdoom updated to version: " + version, "Update Gzdoom",
                                        wx.ICON_INFORMATION)
            else:
                wxdialogs.alertDialog(parent, "Update filed, verify gzdoomLauncher.log form more details.", "Error")
    else:
        if showMessage:
            try:
                progress.Destroy()
            except Exception as e:
                functions.log(e)
            wxdialogs.messageDialog(parent, "Gzdoom is already at latest version!", "Update Gzdoom",
                                    wx.ICON_INFORMATION)

def CheckGzDoomVersion():
    if not os.path.exists(functions.downloadPath):
        os.mkdir(functions.downloadPath)

    if os.name == "nt":
        filename = "gzdoom.zip"
    else:
        filename = "gzdoom.tar.xz"

    localFileName = functions.gzDoomExec

    if os.path.exists(functions.downloadPath + filename):
        os.remove(functions.downloadPath + filename)

    gzdoomUrl = GetGzDoomUrl()
    url = gzdoomUrl[0]
    version = gzdoomUrl[1]
    file = Url(url, filename)
    gameData = gameDefDb.GameDefDb()
    localHash = functions.filehash(localFileName)
    return (os.path.isfile(localFileName)) and (gameData.CheckGzDoomVersion(version, localHash))
