import logging

LOGLEVEL = logging.DEBUG


def log(text, error=True):
    logging.basicConfig(filename='gzDoomLauncher.log', encoding='utf-8', level=LOGLEVEL)
    if error:
        logging.error(text)
    else:
        logging.debug(text)
