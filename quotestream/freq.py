#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import ujson as JSON

from datetime import datetime
from datetime import timedelta

###############################################################################
###############################################################################

def get_args(defaults: dict=frozenset({}),
              parser: argparse.ArgumentParser=None) -> argparse.Namespace:

    return parser.parse_args() \
        if parser else get_args_parser(defaults=defaults).parse_args()

def get_args_parser(defaults: dict=frozenset({})) -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description=
        """
        The *tick frequency* at time t@{i} is defined as f(t@{i}) =
        f(Δt; t@{i}) = 1/Δt·|{t@{j} where t@{j}-Δt < t@{j} < t@{i}}|, where Δt
        is the size of the time interval in which the ticks are counted.
        """, epilog=
        """
        Some researchers found the "log tick frequency," log f(t@{i}), to be
        more relevant. It's also possible to define the average time interval
        between ticks, which is simply the inverse tick f^(-1)(t@{i}). The
        tick frequency is sometimes taken as a proxy for the transaction volume
        on the markets. For various reasons, caution should be applied when
        drawing conclusions on volume from tick frequency though.
        """)

    parser.add_argument("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging(default: %(default)s)")
    parser.add_argument('-i', '--interval', type=float,
        default=defaults['interval'] if 'interval' in defaults else 1.0,
        help='time interval(default: %(default)s [s])')
    parser.add_argument('-r', '--result',
        default=defaults['result'] if 'result' in defaults else [],
        help='result keys(default: %(default)s)')

    return parser

###############################################################################
###############################################################################

class Stack(object):

    def __init__(self, interval: float=0.0) -> None:
        self._list, self._interval = [], timedelta(seconds=interval)

    def __len__(self) -> int:
        return len(self._list)

    def __setitem__(self, key: int, value: datetime) -> None:
        self._list.insert(key, value)
        while self._list[-1] < value - self._interval:
            self._list.pop()

    def put(self, timestamp: datetime) -> None:
        self[0] = timestamp

    @property
    def interval(self) -> float:
        return self._interval.total_seconds()

###############################################################################
###############################################################################

def loop(interval: list, result: list, verbose: bool=False) -> None:

    stack = Stack(interval=eval(interval) if type(interval) is str
        else interval)

    for line in sys.stdin:
        tick = JSON.decode(line.replace("'", '"'))
        now = datetime.fromtimestamp(tick['timestamp'])
        stack.put(now); tick[result] = [len(stack) / stack.interval]

        if verbose: print('[%s] %s' %(now, tick), file=sys.stderr)
        print(tick, file=sys.stdout); sys.stdout.flush()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_args({
        'result': 'freq', 'interval': 600.0 ## 10min
    })

    try: loop(args.interval, args.result, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
