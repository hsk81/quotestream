#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Copies or moves a key with a new name; in both cases the value "
        "remains unchanged. It is possible to bulk copy or rename keys by "
        "repeating the corresponding option multiple times.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-c', '--copy-key', action='append',
        default=[], nargs='+',
        help='copy keys (default: %(default)s)')
    parser.add_argument ('-m', '--move-key', action='append',
        default=[], nargs='+',
        help='move keys (default: %(default)s)')

    return parser.parse_args ()

def loop (copy_map: dict, move_map: dict, verbose: bool=False) -> None:

    pass ## TODO

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    copy_map = dict (args.copy_key)
    move_map = dict (args.move_key)

    try: loop (copy_map, move_map, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
