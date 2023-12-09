import time
import zipfile
import functions
import os

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
        self.maxrange = 100

    def extractAll(self):
        self.message = 'starting'
        for i in range(100):
            self.value += 1
            self.message = 'Progress = ' +  str( self.value)
            time.sleep(1)