import gettext
import hashlib
import logging
import os

from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo
from time import ctime, strftime

LOGLEVEL = logging.ERROR
FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
APPVERSION = "2.03.00"
WINE_GZDOOM = True  # linux gzdoom works only on ubuntu for now.
RE_DOWNLOAD = False

text_color = [1, 1, 1, 1]
highlight_color = [0.5, 0, 0, 1]
background_color = [0, 0, 0, 1]
button_height = 42
button_width = 128


def log(text, error=True):
    text = str(text)
    from dataPath import data_path
    ctime()
    log_text = ''
    if error:
        log_text = '[ERROR] ' + strftime("%Y-%m-%d %H:%M:%S") + ' - ' + text + '\n'
    elif LOGLEVEL == logging.DEBUG:
        log_text = '[DEBUG] ' + strftime("%Y-%m-%d %H:%M:%S") + ' - ' + text + '\n'
    if log_text.strip():
        with open(data_path().logFile, 'a') as log_file:
            log_file.writelines(log_text)
            log_file.close()


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


def set_language(lang):
    if lang not in ('pt_BR'): # Supported languages other than english
        lang = 'en'

    root = os.path.realpath(__file__)
    root = root.replace('functions.py', '')
    locale_path = str(root) + 'locale'
    try:
        file = open(locale_path + '/' + lang + '.po', 'r')
        catalog = read_po(file, locale=lang, domain='gzdl_messages')
        file.close()
        if not os.path.isdir(locale_path + '/' + lang):
            os.mkdir(locale_path + '/' + lang)
        if not os.path.isdir(locale_path + '/' + lang + '/LC_MESSAGES'):
            os.mkdir(locale_path + '/' + lang + '/LC_MESSAGES/')
        file = open(locale_path + '/' + lang + '/LC_MESSAGES/' + catalog.domain + '.mo', 'wb')
        write_mo(file, catalog, True)
        file.close()
        function = gettext.translation('gzdl_messages', locale_path, languages=[lang])
        function.install()
    except Exception as e:
        print(e)
        set_language('en')
