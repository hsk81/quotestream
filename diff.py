#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import sys

from functools import reduce
from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Calculates the difference of corresponding key values between ticks. "
        "It is possible to apply this function on more than one key at the "
        "same time.")

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

    curr_tick = None
    curr_values = None

    for line in sys.stdin:

        last_tick = curr_tick
        last_values = curr_values
        curr_tick = JSON.decode (line.replace ("'", '"'))
        curr_values = [float (curr_tick[key]) for key in in_keys]

        if last_tick:
            for curr, last, key in zip (curr_values, last_values, out_keys):
                curr_tick[key] = curr - last

            if verbose:
                now = datetime.fromtimestamp (curr_tick['timestamp'])
                print ('[%s] %s' % (now, curr_tick), file=sys.stderr)

            print (curr_tick, file=sys.stdout)

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
