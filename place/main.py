# file: main.py
# author: mbiokyle29
import logging
import os
import sys

from click import argument, command, option, Path

from place.lib.utils import is_dir, configure_logger


root_logger = logging.getLogger("")


@command()
@argument("sources", nargs=-1, type=Path(exists=True, resolve_path=True))
@argument("target", nargs=1, type=Path())
@option("-v", "--verbose", default=False, is_flag=True, help="Enable verbose logging.")
@option("-d", "--debug", default=False, is_flag=True, help="Enable debug logging.")
def cli(sources, target, verbose, debug):
    """ mv file(s) in SOURCES to TARGET while updating config files """
    log_level = logging.INFO if verbose else logging.WARN
    log_level = logging.DEBUG if debug else log_level
    configure_logger(root_logger, log_level)

    # rename - 1 source, target must not be a dir
    if len(sources) == 1 and not is_dir(target):
        root_logger.debug("Renaming source file %s to target %s", sources[0], target)
        os.rename(sources[0], target)

    # move - n sources, target must be a dir
    elif len(sources) >= 1 and is_dir(target):
        for source in sources:
            new_path = os.path.join(
                os.path.abspath(target),
                os.path.basename(source)
            )
            root_logger.debug("Moving source file %s to target location %s", source, target)
            os.rename(source, new_path)

    # badness
    else:
        root_logger.warning("No placeable files detected in input. Quitting...")
        sys.exit(-1)
