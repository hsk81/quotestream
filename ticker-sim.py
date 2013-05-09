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
    parser.add_argument ('-M', '--map-from', action='append',
        default=[],
        nargs='+', help='input maps (default: %(default)s)')
    parser.add_argument ('-m', '--map-to', action='append',
        default=[('last', 'price')],
        nargs='+', help='output maps (default: %(default)s)')
    parser.add_argument ('-o', '--out-keys',
        default=['timestamp', 'bid', 'ask', 'price', 'high', 'low', 'volume'],
        nargs='+', help='output keys (default: %(default)s)')
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

def loop (map_from: dict, map_to: dict, out_keys: list,
          from_date: datetime, to_date: datetime,
          acceleration: float, verbose: bool=False) -> None:

    def mapped (key: str, maps: dict) -> str:
        return maps[key] if key in maps else key

    def select (tick: dict, maps: dict, keys: list=None) -> dict: return {
        mapped (k, maps=maps): v for k, v in tick.items ()
            if not keys or mapped (k, maps=maps) in keys
    }

    curr_tick = None
    for line in sys.stdin:

        last_tick = curr_tick
        curr_json = JSON.loads (line.replace ("'", '"'))
        curr_tick = select (curr_json, map_from)

        now = datetime.fromtimestamp (curr_tick['timestamp'])
        if from_date and from_date > now: continue
        if to_date and to_date <= now: break

        if last_tick is not None:
            curr_time = float (curr_tick['timestamp'])
            last_time = float (last_tick['timestamp'])
            time.sleep ((curr_time - last_time) * acceleration)

        if verbose:
            print ('[%s] %s' % (now, curr_json), file=sys.stderr)

        tick = select (curr_tick, map_to, keys=out_keys)
        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.map_from, args.map_to = dict (args.map_from), dict (args.map_to)
    args.from_date = parser.parse (args.from_date) if args.from_date else None
    args.to_date = parser.parse (args.to_date) if args.to_date else None

    try: loop (
        args.map_from, args.map_to, args.out_keys,
        args.from_date, args.to_date,
        args.acceleration,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
