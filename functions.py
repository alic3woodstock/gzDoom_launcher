import logging

LOGLEVEL = logging.DEBUG
FORMAT = '%(asctime)s - %(message)s'


def log(text, error=True):
    logging.basicConfig(filename='gzDoomLauncher.log', encoding='utf-8', level=LOGLEVEL, format=FORMAT)
    if error:
        logging.error(text)
    else:
        logging.debug(text)
