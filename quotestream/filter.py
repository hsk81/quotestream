#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import ujson as JSON

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description=
        """
        Includes or excludes keys: If no include is provided then *all* keys
        are kept except the explicitly excluded. It is not possible to apply
        the include *and* exclude operations simultaneously.
        """)

    parser.add_argument("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging(default: %(default)s)")
    parser.add_argument('-i', '--include-keys', action='append',
        default=[], nargs='+',
        help='include key(s)(default: %(default)s)')
    parser.add_argument('-e', '--exclude-keys', action='append',
        default=[], nargs='+',
        help='exclude key(s)(default: %(default)s)')

    return parser.parse_args()

def loop(include_keys: set, exclude_keys: set, verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode(line.replace("'", '"'))

        if len(exclude_keys) > 0:
            for key in exclude_keys: del tick[key]

        if len(include_keys) > 0:
            tick = {key: tick[key] for key in include_keys}

        if verbose:
            now = datetime.fromtimestamp(tick['timestamp'])
            print('[%s] %s' %(now, tick), file=sys.stderr)

        print(tick, file=sys.stdout); sys.stdout.flush()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments()
    args.include_keys = set([item for ls in args.include_keys for item in ls])
    args.exclude_keys = set([item for ls in args.exclude_keys for item in ls])

    try: loop(args.include_keys, args.exclude_keys, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
