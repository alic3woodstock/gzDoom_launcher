import logging
import hashlib
import os

LOGLEVEL = logging.DEBUG
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "1.00.01"
AUTHOR = "Copyright 2022-2023 © Alice Woodstock"


def log(text, error=True):
    logging.basicConfig(filename='gzDoomLauncher.log', encoding='utf-8', level=LOGLEVEL, format=FORMAT)
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
