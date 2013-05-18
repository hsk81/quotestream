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

    class attach (argparse.Action):
        """Appends values by *overwriting* initial defaults (if any)"""
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr (namespace, self.dest, [])
            if items == self.default:
                setattr (namespace, self.dest, [values])
            else:
                setattr (namespace, self.dest, list (items) + [values])

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')
    parser.add_argument ('-f', '--function', action=attach, nargs='+',
        default=defaults['function'] if 'function' in defaults else [],
        help='map function(s) (default: %(default)s)')
    parser.add_argument ('-p', '--parameter-group', action=attach, nargs='+',
        default=defaults['parameter-group'] if 'parameter-group' in defaults else [],
        help='parameter group *per* result key (default: %(default)s)')
    parser.add_argument ('-r', '--result', action=attach, nargs='+',
        default=defaults['result'] if 'result' in defaults else [],
        help='result keys (default: %(default)s)')

    return process (parser.parse_args ())

def process (args: argparse.Namespace) -> argparse.Namespace:

    args.function = list (
        reduce (lambda a, b: a + b, args.function, []))
    args.result = list (
        reduce (lambda a, b: a + b, args.result, []))
    args.parameter_group = list (map (lambda pg: list (
        filter (lambda p: p != "", pg)), args.parameter_group))

    diff = len (args.result) - len (args.function)
    args.function += [args.function[-1] for _ in range (diff)]
    diff = len (args.result) - len (args.parameter_group)
    args.parameter_group += [[] for _ in range (diff)]

    return args

###############################################################################
###############################################################################

def loop (functions: list, parameter_groups: list, results: list,
          verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for item in zip (functions, parameter_groups, results):
            function, parameter_group, result = item
            args = map (lambda parameter: tick[parameter], parameter_group)
            tick[result] = list (function (*args) if callable (function)
                else eval (function.format (*args)))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

    try: loop (args.function, args.parameter_group, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
