#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import time
import sys
import ujson as JSON

from dateutil import parser
from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        """
        Loops over recorded ticks for simulation and training purposes with
        the possibility to adjust the tick speed. The simulated ticks need to
        be fed via the standard input.
        """)

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ("-f", "--from-date",
        default=None,
        help="date to simulate from (default: %(default)s)")
    parser.add_argument ("-t", "--till-date",
        default=None,
        help="date to simulate till (default: %(default)s)")
    parser.add_argument ("-a", "--acceleration",
        default=1.000, type=float,
        help="time acceleration (default: %(default)s)")

    return parser.parse_args ()

def loop (from_date: datetime, till_date: datetime, acceleration: float,
          verbose: bool=False) -> None:

    curr_tick = None
    for line in sys.stdin:

        last_tick = curr_tick
        curr_tick = JSON.decode (line.replace ("'", '"'))

        now = datetime.fromtimestamp (curr_tick['timestamp'])
        if from_date and from_date > now: continue
        if till_date and till_date <= now: break

        if last_tick is not None:
            curr_time = float (curr_tick['timestamp'])
            last_time = float (last_tick['timestamp'])
            time.sleep ((curr_time - last_time) * acceleration)

        if verbose: print ('[%s] %s' % (now, curr_tick), file=sys.stderr)
        print (curr_tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.from_date = parser.parse (args.from_date) if args.from_date else None
    args.till_date = parser.parse (args.till_date) if args.till_date else None

    try: loop (args.from_date, args.till_date, args.acceleration,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
