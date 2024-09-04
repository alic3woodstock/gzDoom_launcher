import hashlib
import logging
import os

LOGLEVEL = logging.ERROR
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "2.02.00"
AUTHOR = "Copyright 2022-2024 © Alice Woodstock"
WINE_GZDOOM = True  # linux gzdoom works only on ubuntu for now.
RE_DOWNLOAD = False

text_color = [1, 1, 1, 1]
highlight_color = [0.5, 0, 0, 1]
background_color = [0, 0, 0, 1]
button_height = 42
button_width = 128


def log(text, error=True):
    from dataPath import data_path
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
