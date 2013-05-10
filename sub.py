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
        "Calculates the difference of two numbers. It is possible to apply "
        "this function on multiple keys simultaneously.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ("-l", "--in-keys-lhs", action='append',
        default=[], nargs='+',
        help="left hand side input keys (default: %(default)s)")
    parser.add_argument ("-r", "--in-keys-rhs", action='append',
        default=[], nargs='+',
        help="right hand side input keys (default: %(default)s)")
    parser.add_argument ("-o", "--out-keys", action='append',
        default=[], nargs='+',
        help="output keys (default: %(default)s)")

    return parser.parse_args ()

def loop (in_keys_lhs: list, in_keys_rhs: list, out_keys: list,
          verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for l, r, k in zip (in_keys_lhs, in_keys_rhs, out_keys):
            tick[k] = float (tick[l]) - float (tick[r])

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.in_keys_lhs = list (reduce (lambda a, b: a + b, args.in_keys_lhs, []))
    args.in_keys_rhs = list (reduce (lambda a, b: a + b, args.in_keys_rhs, []))
    args.out_keys = list (reduce (lambda a, b: a + b, args.out_keys, []))

    try: loop (args.in_keys_lhs, args.in_keys_rhs, args.out_keys,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
