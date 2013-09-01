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

def get_arguments (defaults: dict=frozenset ({})) -> argparse.Namespace:
    parser = argparse.ArgumentParser ()

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')
    parser.add_argument ('-f', '--function',
        default=defaults['function'] if 'function' in defaults else None,
        help='map function(s) (default: %(default)s)')
    parser.add_argument ('-p', '--parameters', action='append', nargs='+',
        default=defaults['parameters'] if 'parameters' in defaults else [],
        help='function parameter key(s) (default: %(default)s)')
    parser.add_argument ('-r', '--result',
        default=defaults['result'] if 'result' in defaults else 'result',
        help='result key (default: %(default)s)')

    return normalize (parser.parse_args ())

def normalize (args: argparse.Namespace) -> argparse.Namespace:
    args.parameters = reduce (lambda a, b: a + b, args.parameters, [])
    return args

###############################################################################
###############################################################################

def loop (function, parameters, result: list, verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        if callable (function):
            tick[result] = list (function (
                *map (lambda p: tick[p], parameters)
            ).flatten ())
        else:
            tick[result] = list (eval (function.format (
                **{p: tick[p] for p in parameters}
            )).fatten ())

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = get_arguments ()

    try: loop (args.function, args.parameters, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
