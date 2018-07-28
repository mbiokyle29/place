# file: config.py
# author: mbiokyle29
import configparser
import logging
import os.path as path
from pkg_resources import resource_filename


logger = logging.getLogger("place.lib.config")


class PlaceConfig(object):
    """ Encapsulation of configuration options """

    RC_FILE_NAME = ".placerc"

    def __init__(self):
        self._verbose = False
        self._debug = False
        self._log_level = None

    @classmethod
    def readConfigFiles(cls, cwd):
        """ Find and attempt to load settings from config file """
        rc_file_paths = [
            path.join(cwd, cls.RC_FILE_NAME),
            path.join(path.expanduser("~"), cls.RC_FILE_NAME),
            resource_filename("place", path.join("data", cls.RC_FILE_NAME))
        ]

        found_rc_file_paths = [
            rc_file_path for rc_file_path in rc_file_paths
            if path.isfile(rc_file_path)
        ]

        kwargs = {}
        if len(found_rc_file_paths) >= 1:
            rc_file_path = found_rc_file_paths[0]

            logger.debug("Loading config from %s", rc_file_path)
            parser = configparser.ConfigParser()
            parser.read(rc_file_path)

            if "place" in parser:
                kwargs["verbose"] = parser["place"].getboolean("verbose", fallback=False)
                kwargs["debug"] = parser["place"].getboolean("debug", fallback=False)

        logger.debug("Creating with: %s", kwargs)
        return kwargs

    @classmethod
    def fromKwargs(cls, **kwargs):
        """ Create a config instance from kwargs """
        instance = cls()
        instance._verbose = bool(kwargs.get("verbose", False))
        instance._debug = bool(kwargs.get("debug", False))

        return instance

    @property
    def verbose(self):
        return self._verbose

    @property
    def debug(self):
        return self._debug

    @property
    def log_level(self):
        if self._log_level is None:
            log_level = logging.INFO if self._verbose else logging.WARN
            log_level = logging.DEBUG if self._debug else log_level
            self._log_level = log_level

        return self._log_level
