# file: utils.py
# author: mbiokyle29
import logging
import os.path as path


logger = logging.getLogger("place.lib.utils")


def is_dir(input_path):
    """ Return a boolean if the path is not a dir """
    abs_path = path.abspath(input_path)
    logger.debug("Checking if path: %s is a directory", abs_path)
    return path.isdir(abs_path)


def configure_logger(logger, level):
    logger.setLevel(level)
    sh = logging.StreamHandler()
    sh.setLevel(level)
    formatter = logging.Formatter("[%(name)s][%(levelname)s]: %(message)s")
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger
