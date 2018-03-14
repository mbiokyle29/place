# file: utils.py
# author: mbiokyle29
import os.path as path


def is_dir(input_path):
    """ Return a boolean if the path is not a dir """
    abs_path = path.abspath(input_path)
    return path.isdir(abs_path)
