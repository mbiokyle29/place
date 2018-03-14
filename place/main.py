# file: main.py
# author: mbiokyle29
import os
import sys

from click import argument, command, Path

from place.lib.utils import is_dir


@command()
@argument("sources", nargs=-1, type=Path(exists=True, resolve_path=True))
@argument("target", nargs=1, type=Path())
def cli(sources, target):
    """ mv file(s) in SOURCES to TARGET while updating config files """

    # rename - 1 source, target must not be a dir
    if len(sources) == 1 and not is_dir(target):
        os.rename(sources[0], target)

    # move - n sources, target must be a dir
    elif len(sources) >= 1 and is_dir(target):
        for source in sources:
            new_path = os.path.join(
                os.path.abspath(target),
                os.path.basename(source)
            )
            os.rename(source, new_path)

    # badness
    else:
        sys.exit(-1)
