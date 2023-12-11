import time
import zipfile
import functions
import os
import requests

from kivy.clock import Clock
from gameDefDb import GameDefDb
from url import Url

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


class GameFile():
    def __init__(self):
        self.value = 0
        self.message = 'Starting ...'
        self.max_range = 100
        self.clock = None
        self.totalDownloads = 0
        self.currentDownload = 0
        self.done = False

    def extractAll(self):
        self.message = 'Downloading files...'

        dataCon = GameDefDb()

        if not os.path.exists(functions.downloadPath):
            os.mkdir(functions.downloadPath)


        urls = dataCon.SelectDefaultUrls()

        # Total downloads + gzdoom
        self.max_range = len(urls) + 1
        self.totalDownloads = len(urls) + 1
        for u in urls:
            self.DownloadFile(u)
            self.value += 1

        self.message = 'Updating gzdoom...'
        update = self.UpdateGzDoom()
        self.value += 1
        if not update:
            functions.log('Update gzdoom failed', True)

        self.message = 'All done, have fun!'
        self.value = self.max_range
        self.done = True

        # if self.clock:
        #     self.clock()
        #     Clock.unschedule(self.clock.get_callback())

    def DownloadFile(self, url):
        # updates dialog based on a fixed max range since I don't know the total size of all files before download
        # each file.
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
                            strTotal = str(total_length // 1024)
                        else:
                            strTotal = "..."
                        downloadF.write(chunk)
                    i += 1024

                    self.message = "Downloading file " + str(self.currentDownload) \
                                   + "/" + str(self.totalDownloads) + ": " \
                                   + str(i // 1024) + "k of " + strTotal + "k"

        self.currentDownload += 1

    def UpdateGzDoom(self):
        if not os.path.exists(functions.downloadPath):
            os.mkdir(functions.downloadPath)

        if os.name == "nt":
            filename = "gzdoom.zip"
        else:
            filename = "gzdoom.tar.xz"

        localFileName = functions.gzDoomExec

        if os.path.exists(functions.downloadPath + filename):
            os.remove(functions.downloadPath + filename)

        gzdoomUrl = self.GetGzDoomUrl()
        url = gzdoomUrl[0]
        version = gzdoomUrl[1]
        file = Url(url, filename)
        gameData = GameDefDb()
        localHash = functions.filehash(localFileName)

        if (not os.path.isfile(localFileName)) or (not gameData.CheckGzDoomVersion(version, localHash)):
            self.DownloadFile(file)

            if os.name == "nt":
                zipfile = ZipFile(filename, "zip")
            else:
                zipfile = ZipFile(filename, "xz")

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
                        # if showMessage:
                        #     progress.Destroy()
                    except Exception as e:
                        functions.log(e)
                gameData.UpdateGzdoomVersion(version, localHash)
                if os.path.exists(functions.tempDir):
                    shutil.rmtree(functions.tempDir)

            result = extractOK and (os.path.isfile(functions.gzDoomExec)
                                    or os.path.isfile(functions.gzDoomExec))
        else:
            result = True

        return result

    def GetGzDoomUrl(self):
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
        end = tmpStr.lower().find('" rel=')

        tmpStr = "https://github.com" + tmpStr[:end].strip()
        functions.log(tmpStr, False)
        return [tmpStr, version]
