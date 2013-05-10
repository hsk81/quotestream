#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import sys

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Includes or excludes keys: If no include is provided then *all* keys "
        "are kept except the explicitly excluded. It is not possible to apply "
        "the include *and* exclude operations simultaneously.")

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

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        if len (exclude_keys) > 0:
            for key in exclude_keys: del tick[key]

        if len (include_keys) > 0:
            tick = {key: tick[key] for key in include_keys}

        print (tick, file=sys.stdout); sys.stdout.flush ()

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
