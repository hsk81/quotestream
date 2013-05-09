#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import json as JSON
import argparse
import time
import sys

from dateutil import parser
from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Loops over recorded ticks for simulation and training purposes with "
        "the possibility to adjust the tick speed as desired.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-o', '--out-keys',
        default=['timestamp', 'bid', 'ask', 'price', 'high', 'low', 'volume'],
        nargs='+', help='output keys (default: %(default)s)')
    parser.add_argument ('-m', '--map-to', action='append',
        default=[('last', 'price')],
        nargs='+', help='output maps (default: %(default)s)')
    parser.add_argument ("-f", "--from-date",
        default=None,
        help="date to begin from (default: %(default)s)")
    parser.add_argument ("-t", "--to-date",
        default=None,
        help="date to stop at (default: %(default)s)")
    parser.add_argument ("-a", "--acceleration",
        default=1.000, type=float,
        help="time acceleration (default: %(default)s)")

    return parser.parse_args ()

def loop (out_keys: list, out_maps: dict,
          from_date: datetime, to_date: datetime,
          acceleration: float, verbose: bool=False) -> None:

    def mapped (key: str) -> str:
        return out_maps[key] if key in out_maps else key

    def select (tick: dict) -> dict: return {
        mapped (k): v for k, v in tick.items () if mapped (k) in out_keys
    }

    curr_tick = None
    for line in sys.stdin:

        last_tick, curr_tick = curr_tick, JSON.loads (line.replace ("'", '"'))
        now = datetime.fromtimestamp (curr_tick['timestamp'])
        if from_date and from_date > now: continue
        if to_date and to_date <= now: break

        if last_tick is not None:
            curr_time = float (curr_tick['timestamp'])
            last_time = float (last_tick['timestamp'])
            time.sleep ((curr_time - last_time) * acceleration)

        tick = select (curr_tick)
        if verbose: print ('[%s] %s' % (now, tick), file=sys.stderr)
        print (tick, file=sys.stdout)

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.map_to = dict (args.map_to)
    args.from_date = parser.parse (args.from_date) if args.from_date else None
    args.to_date = parser.parse (args.to_date) if args.to_date else None

    try: loop (args.out_keys, args.map_to, args.from_date, args.to_date,
        args.acceleration, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
