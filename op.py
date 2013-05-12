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
from numpy import *

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Evaluates provided functions which can have multiple parameters and "
        "stores the results in the corresponding keys. If there are less "
        "functions than result keys than the last one will be used for the "
        "remaining results. The parameters for each function need to be "
        "provided as a group. Empty groups can either be left out or they can "
        "be indicated by an empty string (used with functions without "
        "parameters). String interpolation is based on Python's `format`.")

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')
    parser.add_argument ('-p', '--parameter-group', action='append',
        default=[], nargs='+',
        help='parameter group *per* result key (default: %(default)s)')
    parser.add_argument ('-f', '--function', action='append',
        default=[], nargs='+',
        help='function(s) to evaluate (default: %(default)s)')
    parser.add_argument ('-r', '--result', action='append',
        default=[], nargs='+',
        help='result keys (default: %(default)s)')

    return parser.parse_args ()

def loop (functions: list, parameter_groups: list, results: list,
          verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))

        for pg, res, fn in zip (parameter_groups, results, functions):
            tick[res] = eval (fn.format (*map (lambda p: tick[p], pg)))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

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

    try: loop (args.function, args.parameter_group, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
