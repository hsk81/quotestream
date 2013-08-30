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
    parser.add_argument ('-p', '--parameter',
        default=defaults['parameter'] if 'parameter' in defaults else 'timestamp',
        help='function parameter (default: %(default)s)')
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

    def put (self, item: float or list) -> None:

        self._list[self._size - 1:] = []
        self._list.insert (0, item[0] if isinstance (item, list) else item)

    @property
    def all (self) -> list:

        return array (self._list)

    @property
    def full (self) -> bool:

        return len (self._list) >= self._size

###############################################################################
###############################################################################

def loop (function, parameter, stack_size, default, result: list,
          verbose: bool=False) -> None:

    stack_t = Stack (size=stack_size)
    stack_v = Stack (size=stack_size)
    tick = None

    for line in sys.stdin:
        last, tick = tick, JSON.decode (line.replace ("'", '"'))

        stack_t.put (tick['timestamp'])
        stack_v.put (tick[parameter])

        if stack_v.full:
            if callable (function):
                tick[result] = list (function (stack_t.all, stack_v.all,
                    last[result] if last
                        else list (eval (default) if type (default) is str
                            else default)
                ).flatten ())
            else:
                tick[result] = list (eval (function.format (
                    ts=stack_t.all,
                    values=stack_v.all,
                    last=last[result] if last
                        else list (eval (default) if type (default) is str
                            else default)
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

    try: loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
