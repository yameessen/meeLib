"""

*/meeLib.logger
    Logger settings of the meeLib library

"""

import logging
import inspect


# region Main
def _get_caller_logger():
    frame = inspect.currentframe()
    outer = frame.f_back
    module = inspect.getmodule(outer)
    name = module.__name__ if module else __name__
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s] %(levelname)s - %(filename)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    return logger


logger = _get_caller_logger()

# endregion
