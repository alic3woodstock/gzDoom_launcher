from os import path, makedirs, name as os_name
from sys import argv
from functions import WINE_GZDOOM

dataPath = None


def data_path():
    global dataPath
    return dataPath


class DataPath:
    def __init__(self):
        global dataPath
        
        self.data = path.realpath(__file__)
        self.pentagram = self.data.replace("dataPath.py", "pentagram.png")
        if len(argv) > 1 and argv[1].strip() == '-datapath' and argv[2].strip():
            self.data = argv[2].strip()
        else:
            self.data = self.data.replace("dataPath.py", "data")

        # global paths
        self.db = self.data + "/games.sqlite3"
        self.gzDoom = self.data + "/gzdoom/"
        self.temp = self.data + "/temp/"
        self.download = self.data + "/downloads/"
        self.wad = self.data + "/wads/"
        self.map = self.data + "/maps/"
        self.mod = self.data + "/mods/"

        # global files
        self.logFile = self.data + '/gzDoomLauncher.log'

        if WINE_GZDOOM:
            self.gzDoomExec = self.gzDoom + "gzdoom.exe"
        else:
            self.gzDoomExec = self.gzDoom + "gzdoom"

        self.wine = self.gzDoom + 'lutris-GE-Proton8-26-x86_64/bin/wine64'

        if not path.exists(self.data):
            makedirs(self.data)

        if os_name == "nt":
            self.db = self.db.replace('/', '\\')
            self.gzDoom = self.gzDoom.replace('/', '\\')
            self.temp = self.temp.replace('/', '\\')
            self.download = self.download.replace('/', '\\')
            self.wad = self.wad.replace('/', '\\')
            self.map = self.map.replace('/', '\\')
            self.mod = self.mod.replace('/', '\\')

            self.logFile = self.logFile.replace('/', '\\')
            self.gzDoomExec = self.gzDoom + "gzdoom.exe"
            self.pentagram = self.pentagram.replace('/', '\\')

        dataPath = self
