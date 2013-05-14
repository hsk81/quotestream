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

    parser = argparse.ArgumentParser (description=
        "Reduces a stack of previously seen parameter values using a function "
        "to a result. It is possible to access within the evaluator the value "
        "of the *most recent* result by referencing another interpolation "
        "index: The latter option is convenient to calculate e.g. moving "
        "averages.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-f', '--function', action='append',
        default=[], nargs='+',
        help='reduce function(s) (default: %(default)s)')
    parser.add_argument ('-p', '--parameter', action='append',
        default=[], nargs='+',
        help='function parameter(s) (default: %(default)s)')
    parser.add_argument ('-n', '--stack-size', action='append',
        default=[], nargs='+', type=int,
        help='stack of previously seen values (default: %(default)s)')
    parser.add_argument ('-d', '--default', action='append',
        default=[], nargs='+',
        help='default result(s) (default: %(default)s)')
    parser.add_argument ('-r', '--result', action='append',
        default=[], nargs='+',
        help='result keys (default: %(default)s)')

    return parser.parse_args ()

###############################################################################
###############################################################################

class Stack (object):

    def __init__ (self, size: int=0) -> None:

        self._list = []
        self._size = size

    def put (self, item: object) -> None:

        self._list[self._size - 1:] = []
        self._list.insert (0, item)

    @property
    def all (self) -> list:

        return self._list

    @property
    def full (self) -> bool:

        return len (self._list) >= self._size

###############################################################################
###############################################################################

def loop (functions: list, parameters: list, stack_sizes: list, defaults: list,
          results: list, verbose: bool=False) -> None:

    stacks = [Stack (size=size) for size in stack_sizes]
    tick = None

    for line in sys.stdin:
        last, tick = tick, JSON.decode (line.replace ("'", '"'))

        for item in zip (stacks, functions, parameters, defaults, results):
            stack, function, parameter, default, result = item
            stack.put (tick[parameter])

            if stack.full:
                args = stack.all + [last[result] if last else default]
                tick[result] = eval (function.format (*args))
            else:
                tick[result] = default

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout)

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.function = list (reduce (lambda a, b: a + b, args.function, []))
    args.parameter = list (reduce (lambda a, b: a + b, args.parameter, []))
    args.stack_size = list (reduce (lambda a, b: a + b, args.stack_size, []))
    args.default = list (reduce (lambda a, b: a + b, args.default, []))
    args.result = list (reduce (lambda a, b: a + b, args.result, []))

    diff = len (args.result) - len (args.function)
    args.function += [args.function[-1] for _ in range (diff)]
    diff = len (args.result) - len (args.parameter)
    args.parameter += [args.parameter[-1] for _ in range (diff)]
    diff = len (args.result) - len (args.stack_size)
    args.stack_size += [args.stack_size[-1] for _ in range (diff)]
    diff = len (args.result) - len (args.default)
    args.default += [None for _ in range (diff)]

    try: loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
