import logging
import hashlib
import os

LOGLEVEL = logging.DEBUG
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'


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
