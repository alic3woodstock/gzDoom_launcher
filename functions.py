import hashlib
import logging
import os
from dataPath import data_path

LOGLEVEL = logging.ERROR
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "2.01.00"
AUTHOR = "Copyright 2022-2024 © Alice Woodstock"
WINE_GZDOOM = True  # linux gzdoom works only on ubuntu for now.
RE_DOWNLOAD = False

# dbPath = "games.sqlite3"
# gzDoomPath = "gzdoom/"
# tempDir = "temp/"
# downloadPath = "downloads/"
# wadPath = "wads/"
# mapPath = "maps/"
# modPath = "mods/"
# gzDoomExec = "gzdoom/gzdoom"
# logFile = "gzdlauncher.log"
# pentagram = "pentagram.png"
# dataPath = 'data'
# rootFolder = ""

text_color = [1, 1, 1, 1]
highlight_color = [0.5, 0, 0, 1]
background_color = [0, 0, 0, 1]
button_height = 42
button_width = 128


def log(text, error=True):
    log_file = logging.getLogger(__name__)
    logging.basicConfig(filename=data_path().logFile, encoding='utf-8', level=LOGLEVEL, format=FORMAT)
    if error:
        log_file.error(text)
    else:
        log_file.debug(text)


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


def version_number():
    str_version = APPVERSION.replace(".", "")
    return int(str_version)


# def setDataPath():
#     global dbPath
#     global gzDoomPath
#     global tempDir
#     global downloadPath
#     global wadPath
#     global mapPath
#     global modPath
#     global gzDoomExec
#     global logFile
#     global pentagram
#     global rootFolder
#     global dataPath
#
#     dataPath = os.path.realpath(__file__)
#     pentagram = dataPath.replace("functions.py", "pentagram.png")
#     rootFolder = dataPath.replace("functions.py", "")
#     if len(sys.argv) > 1 and sys.argv[1].strip() == '-datapath' and sys.argv[2].strip():
#         dataPath = sys.argv[2].strip()
#     else:
#         dataPath = dataPath.replace("functions.py", "data")
#
#     # global paths
#     dbPath = dataPath + "/games.sqlite3"
#     gzDoomPath = dataPath + "/gzdoom/"
#     tempDir = dataPath + "/temp/"
#     downloadPath = dataPath + "/downloads/"
#     wadPath = dataPath + "/wads/"
#     mapPath = dataPath + "/maps/"
#     modPath = dataPath + "/mods/"
#
#     # global files
#     logFile = dataPath + '/gzDoomLauncher.log'
#     gzDoomExec = gzDoomPath + "gzdoom"
#
#     if not os.path.exists(dataPath):
#         os.makedirs(dataPath)
#
#     if os.name == "nt":
#         dbPath = dbPath.replace('/', '\\')
#         gzDoomPath = gzDoomPath.replace('/', '\\')
#         tempDir = tempDir.replace('/', '\\')
#         downloadPath = downloadPath.replace('/', '\\')
#         wadPath = wadPath.replace('/', '\\')
#         mapPath = mapPath.replace('/', '\\')
#         modPath = modPath.replace('/', '\\')
#
#         logFile = logFile.replace('/', '\\')
#         gzDoomExec = gzDoomPath + "gzdoom.exe"
#         pentagram = pentagram.replace('/', '\\')
