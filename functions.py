import hashlib
import logging
import os

LOGLEVEL = logging.ERROR
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "2.00.00"
AUTHOR = "Copyright 2022-2023 © Alice Woodstock"

dbPath = "games.sqlite3"
gzDoomPath = "gzdoom/"
tempDir = "temp/"
downloadPath = "downloads/"
wadPath = "wads/"
mapPath = "maps/"
modPath = "mods/"
gzDoomExec = "gzdoom/gzdoom"
logFile = "gzdlauncher.log"
pentagram = "pentagram.png"
rootFolder = ""


def log(text, error=True):
    logging.basicConfig(filename=logFile, encoding='utf-8', level=LOGLEVEL, format=FORMAT)
    if error:
        logging.error(text)
    else:
        logging.debug(text)


def filehash(file_name):
    sha256hash = ""
    if os.path.isfile(file_name):
        try:
            with open(file_name, 'rb') as f:
                data = f.read()
                sha256hash = hashlib.sha256(data).hexdigest()
        except Exception as e:
            log(e)
    return sha256hash


def versionNumber():
    strVersion = APPVERSION.replace(".", "")
    return int(strVersion)


def setDataPath():
    global dbPath
    global gzDoomPath
    global tempDir
    global downloadPath
    global wadPath
    global mapPath
    global modPath
    global gzDoomExec
    global logFile
    global pentagram
    global rootFolder

    dataPath = os.path.realpath(__file__)
    pentagram = dataPath.replace("functions.py", "pentagram.png")
    rootFolder = dataPath.replace("functions.py", "")
    dataPath = dataPath.replace("functions.py", "data")

    # global paths
    dbPath = dataPath + "/games.sqlite3"
    gzDoomPath = dataPath + "/gzdoom/"
    tmpDir = dataPath + "/temp/"
    downloadPath = dataPath + "/downloads/"
    wadPath = dataPath + "/wads/"
    mapPath = dataPath + "/maps/"
    modPath = dataPath + "/mods/"

    # global files
    logFile = dataPath + '/gzDoomLauncher.log'
    gzDoomExec = gzDoomPath + "gzdoom"

    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

    if os.name == "nt":
        dbPath = dbPath.replace('/', '\\')
        gzDoomPath = gzDoomPath.replace('/', '\\')
        tmpDir = tmpDir.replace('/', '\\')
        downloadPath = downloadPath.replace('/', '\\')
        wadPath = wadPath.replace('/', '\\')
        mapPath = mapPath.replace('/', '\\')
        modPath = modPath.replace('/', '\\')

        logFile = logFile.replace('/', '\\')
        gzDoomExec = gzDoomPath + "gzdoom.exe"
        pentagram = pentagram.replace('/', '\\')


text_color = [1, 1, 1, 1]
highlight_color = [0.5, 0, 0, 1]
background_color = [0, 0, 0, 1]
button_height = 42
button_width = 128
