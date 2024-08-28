from os import path, makedirs, name as os_name
from sys import argv

dataPath = None


def data_path():
    global dataPath
    return dataPath


class DataPath:
    def __init__(self):
        global dataPath
        self.db = "games.sqlite3"
        self.gzDoom = "gzdoom/"
        self.temp = "temp/"
        self.download = "downloads/"
        self.wad = "wads/"
        self.map = "maps/"
        self.mod = "mods/"
        self.gzDoomExec = "gzdoom/gzdoom"
        self.logFile = "gzdlauncher.log"
        self.pentagram = "pentagram.png"
        self.data = 'data'
        self.set_data_path()
        dataPath = self

    def set_data_path(self):
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
        self.gzDoomExec = self.gzDoom + "gzdoom"

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
