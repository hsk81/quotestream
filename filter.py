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
        "Includes or excludes keys: If no include is provided then *all* keys "
        "are kept except the explicitly excluded which cannot be re-included, "
        "i.e. exclude has precedence over include.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-i', '--include-key', action='append',
        default=[], nargs='+',
        help='include key(s) (default: %(default)s)')
    parser.add_argument ('-e', '--exclude-key', action='append',
        default=[], nargs='+',
        help='exclude key(s) (default: %(default)s)')

    return parser.parse_args ()

def loop (include_keys: list, exclude_keys: list, verbose: bool=False) -> None:

    pass ## TODO

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

    include_keys = list (
        dict ([(item, 0) for ls in args.include_key for item in ls]))
    exclude_keys = list (
        dict ([(item, 0) for ls in args.exclude_key for item in ls]))

    try: loop (include_keys, exclude_keys, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
