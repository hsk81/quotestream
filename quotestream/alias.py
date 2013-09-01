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

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        """
        Copies or moves a key with a new name; in both cases the value
        remains unchanged. It is possible to bulk copy or rename keys by
        repeating the corresponding option multiple times.
        """)

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-c', '--copy-key', action='append',
        default=[], nargs='+',
        help='key pair to copy from/to (default: %(default)s)')
    parser.add_argument ('-m', '--move-key', action='append',
        default=[], nargs='+',
        help='key pair to move from/to (default: %(default)s)')

    return parser.parse_args ()

def loop (copy_map: dict, move_map: dict, verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for source_key, target_key in copy_map.items ():
            tick[target_key] = tick[source_key]

        for source_key, target_key in move_map.items ():
            tick[target_key] = tick[source_key]
            del tick[source_key]

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

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
