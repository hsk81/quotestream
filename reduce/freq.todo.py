#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import sys

from datetime import datetime, timedelta
from functools import reduce
from numpy import log

###############################################################################
###############################################################################

def get_args (defaults: dict=frozenset ({}),
              parser: argparse.ArgumentParser=None) -> argparse.Namespace:

    return parser.parse_args () \
        if parser else get_args_parser (defaults=defaults).parse_args ()

def get_args_parser (defaults: dict=frozenset ({})) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser ()

    class attach (argparse.Action):
        """Appends values by *overwriting* initial defaults (if any)"""
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr (namespace, self.dest, [])
            if items == self.default:
                setattr (namespace, self.dest, [values])
            else:
                setattr (namespace, self.dest, list (items) + [values])

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-i', '--interval', action=attach, nargs='+',
        default=defaults['interval'] if 'interval' in defaults else [],
        help='time interval (default: %(default)s [s])')
    parser.add_argument ('-r', '--result', action=attach, nargs='+',
        default=defaults['result'] if 'result' in defaults else [],
        help='result keys (default: %(default)s)')

    return parser

def normalize (args: argparse.Namespace) -> argparse.Namespace:

    args.interval = list (reduce (lambda a, b: a + b, args.interval, []))
    args.result = list (reduce (lambda a, b: a + b, args.result, []))

    diff = len (args.result) - len (args.interval)
    args.interval += [args.interval[-1] for _ in range (diff)]
    return args

###############################################################################
###############################################################################

class Stack (object):

    def __init__ (self, interval: float=0.0) -> None:

        self._list, self._interval = [], timedelta (seconds=interval)

    def __len__ (self) -> int:

        return len (self._list)

    def put (self, timestamp: datetime) -> None:

        self._list.insert (0, timestamp)
        while self._list[-1] < timestamp - self._interval:
            self._list.pop ()

    @property
    def interval (self) -> float:

        return self._interval.total_seconds ()

###############################################################################
###############################################################################

def loop (intervals: list, results: list, verbose: bool=False) -> None:

    stacks = [Stack (interval=interval) for interval in map (lambda i: eval (i)
        if type (i) is str else i, intervals)]

    for line in sys.stdin:
        tick = JSON.decode (line.replace ("'", '"'))
        now = datetime.fromtimestamp (tick['timestamp'])

        for stack, result in zip (stacks, results):
            stack.put (now); tick[result] = [len (stack) / stack.interval]

        if verbose:
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = normalize (get_args ({
        'interval': [[600.0]] ## [s] == 10 minutes
    }))

    try: loop (args.interval, args.result, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
