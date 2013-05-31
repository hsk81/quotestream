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
from functools import reduce
from numpy import *

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:
    parser = argparse.ArgumentParser ()

    class attach (argparse.Action):
        """Appends values by *overwriting* initial defaults (if any)"""
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr (namespace, self.dest, [])
            if items == self.default:
                setattr (namespace, self.dest, [values])
            else:
                setattr (namespace, self.dest, list (items) + [values])

    parser.add_argument ("-v", "--verbose", action="store_true",
        default=False, help="verbose logging (default: %(default)s)")
    parser.add_argument ('-n', '--numerator', action=attach, nargs='+',
        default=[], help='numerator (default: %(default)s)')
    parser.add_argument ('-d', '--denominator', action=attach, nargs='+',
        default=[], help='denominator (default: %(default)s)')
    parser.add_argument ('-r', '--result', action=attach, nargs='+',
        default=[], help='result (default: %(default)s)')

    return parser.parse_args ()

def normalize (args: argparse.Namespace) -> argparse.Namespace:

    args.numerator = list (reduce (lambda a, b: a + b, args.numerator, []))
    args.denominator = list (reduce (lambda a, b: a + b, args.denominator, []))
    args.result = list (reduce (lambda a, b: a + b, args.result, []))

    diff = len (args.result) - len (args.numerator)
    args.numerator += [args.numerator[-1] for _ in range (diff)]
    diff = len (args.result) - len (args.denominator)
    args.denominator += [args.denominator[-1] for _ in range (diff)]

    return args

###############################################################################
###############################################################################

def loop (numerators: list, denominators: list, results: list,
          verbose: bool=False) -> None:

    last_numerator = {}
    last_denominator = {}

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for i, item in enumerate (zip (numerators, denominators, results)):
            numerator, denominator, result = item

            if numerator in tick:
                last_numerator[i] = array (tick[numerator])

            if denominator in tick:
                last_denominator[i] = array (tick[denominator])

            if i in last_numerator and i in last_denominator:
                tick[result] = list (last_numerator[i] / last_denominator[i])

                if verbose:
                    now = datetime.fromtimestamp (tick['timestamp'])
                    print ('[%s] %s' % (now, tick), file=sys.stderr)

                print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args = normalize (args)

    try: loop (args.numerator, args.denominator, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
