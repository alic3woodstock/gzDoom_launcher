import logging


def log(text, error=True):
    logging.basicConfig(filename='errors.log', encoding='utf-8', level=logging.INFO)
    if error:
        logging.error(text)
    else:
        logging.info(text)
