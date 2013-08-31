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

def get_args (defaults: dict=frozenset ({}),
              parser: argparse.ArgumentParser=None) -> argparse.Namespace:

    return parser.parse_args () \
        if parser else get_args_parser (defaults=defaults).parse_args ()

def get_args_parser (defaults: dict=frozenset ({})) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser ()

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-f', '--function',
        default=defaults['function'] if 'function' in defaults else None,
        help='reduction function (default: %(default)s)')
    parser.add_argument ('-p', '--parameters', action='append', nargs='+',
        default=defaults['parameters'] if 'parameters' in defaults else [],
        help='function parameter(s) (default: %(default)s)')
    parser.add_argument ('-n', '--stack-size', type=int,
        default=defaults['stack-size'] if 'stack-size' in defaults else 1,
        help='size of stack of recent values (default: %(default)s)')
    parser.add_argument ('-d', '--default',
        default=defaults['default'] if 'default' in defaults else [0.0],
        help='reduction base (default: %(default)s)')
    parser.add_argument ('-r', '--result',
        default=defaults['result'] if 'result' in defaults else 'result',
        help='result key (default: %(default)s)')

    return parser

###############################################################################
###############################################################################

class Stack (object):

    def __init__ (self, size: int=0) -> None:
        self._list = []
        self._size = size

    def __getitem__ (self, item: int) -> float:
        return self._list[item]

    @property
    def top (self) -> float:
        return self[0]

    def __setitem__ (self, key: int, item: float) -> None:
        self._list[self._size - 1:] = []
        self._list.insert (key, item)

    def put (self, item: float or list) -> None:
        if isinstance (item, list):
            self[0] = item[0]
        else:
            self[0] = item

    @property
    def as_array (self) -> list:
        return array (self._list)

    @property
    def is_full (self) -> bool:
        return len (self._list) >= self._size

###############################################################################
###############################################################################

def loop (function, parameters, stack_size, default, result: list,
          verbose: bool=False) -> None:

    parameters = reduce (lambda a, b: a + b, parameters)
    stacks = [Stack (size=stack_size) for _ in parameters]
    tick = None

    for line in sys.stdin:
        last, tick = tick, JSON.decode (line.replace ("'", '"'))
        for parameter, stack in zip (parameters, stacks):
            stack.put (tick[parameter])

        if stacks[0].is_full:
            last_result = last[result] if last \
                else list (eval (default) if type (default) is str
                    else default)

            if callable (function):
                tick[result] = list (function (
                    *map (lambda s: s.as_array, stacks), last=last_result
                ).flatten ())
            else:
                tick[result] = list (eval (function.format (last=last_result,
                    **{p: s.as_array for p, s in zip (parameters, stacks)}
                )).flatten ())
        else:
            tick[result] = list (eval (default) if type (default) is str
                else default)

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = get_args ()

    try: loop (args.function, args.parameters, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
