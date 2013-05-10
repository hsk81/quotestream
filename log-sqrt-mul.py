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
        "Calculates the logarithm of a square root of a multiplication of two "
        "numbers. It is possible to apply this calculation for multiple keys "
        "simultaneously.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ("-l", "--left-keys", action='append',
        default=[], nargs='+',
        help="left hand side keys (default: %(default)s)")
    parser.add_argument ("-r", "--right_keys", action='append',
        default=[], nargs='+',
        help="right hand side keys (default: %(default)s)")
    parser.add_argument ("-t", "--target-keys", action='append',
        default=[], nargs='+',
        help="target keys (default: %(default)s)")

    return parser.parse_args ()

def loop (left_keys: list, right_keys: list, target_keys: list,
          verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for l, r, t in zip (left_keys, right_keys, target_keys):
            tick[t] = math.log (math.sqrt (float (tick[l]) * float (tick[r])))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.left_keys = list (reduce (lambda a, b: a + b, args.left_keys, []))
    args.right_keys = list (reduce (lambda a, b: a + b, args.right_keys, []))
    args.target_keys = list (reduce (lambda a, b: a + b, args.target_keys, []))

    try: loop (args.left_keys, args.right_keys, args.target_keys,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
