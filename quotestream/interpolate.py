#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import ujson as JSON

from datetime import datetime, timedelta
from time import mktime

###############################################################################
###############################################################################

def get_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description=
        """
        Transforms an inhomogeneous time series to a homogeneous one by
        re-delivering the most recent tick in regular intervals.
        """)

    parser.add_argument("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging(default: %(default)s)")
    parser.add_argument("-i", "--interval",
        default=1.000, type=float,
        help="homogeneity interval(default: %(default)s [s])")

    return parser.parse_args()

###############################################################################
###############################################################################

def loop(interval: timedelta, verbose: bool=False) -> None:

    line = sys.stdin.readline()
    tick = JSON.decode(line.replace("'", '"'))
    tick_ts = datetime.fromtimestamp(tick['timestamp'])
    zero_ts = tick_ts
    index = 0

    for line in sys.stdin:

        while True:
            now = zero_ts + index * interval
            if now > tick_ts: break
            tick['timestamp'] = mktime(now.utctimetuple())

            if verbose: print('[%s] %s' %(now, tick), file=sys.stderr)
            print(tick, file=sys.stdout); sys.stdout.flush()
            index += 1

        tick = JSON.decode(line.replace("'", '"'))
        tick_ts = datetime.fromtimestamp(tick['timestamp'])

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments()
    interval = timedelta(seconds=args.interval)

    try: loop(interval=interval, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
