#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import math
import sys

from functools import reduce
from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Calculates the logarithm of a number. It is possible to apply this "
        "function on multiple keys simultaneously.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ("-i", "--in-keys", action='append',
        default=[], nargs='+',
        help="input keys (default: %(default)s)")
    parser.add_argument ("-o", "--out-keys", action='append',
        default=[], nargs='+',
        help="output keys (default: %(default)s)")

    return parser.parse_args ()

def loop (in_keys: list, out_keys: list, verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for in_key, out_key in zip (in_keys, out_keys):
            tick[out_key] = math.log (float (tick[in_key]))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.in_keys = list (reduce (lambda a, b: a + b, args.in_keys, []))
    args.out_keys = list (reduce (lambda a, b: a + b, args.out_keys, []))

    try: loop (args.in_keys, args.out_keys, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
