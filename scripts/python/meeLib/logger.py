"""

*/meeLib.logger
    logger settings of the meeLib library

"""

import logging


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s[%(levelname)s]%(filename)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    return logger
