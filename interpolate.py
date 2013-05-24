#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import time
import sys

from datetime import datetime, timedelta
from threading import Thread, Lock

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        "Transforms an inhomogeneous time series to a homogeneous one by "
        "re-delivering the most recent tick in regular intervals.")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ("-i", "--interval",
        default=1.000, type=float,
        help="homogeneity interval (default: %(default)s [s])")

    return parser.parse_args ()

###############################################################################
###############################################################################

class ConcurrentStack (object):

    def __init__ (self, size: int=0) -> None:

        self._lock = Lock ()
        self._size = size
        self._list = []

    def put (self, item: object) -> None:

        with self._lock:
            self._list[self._size - 1:] = []
            self._list.insert (0, item)

    def top (self, default: object=None) -> object:

        with self._lock:
            return self._list[0] if len (self._list) > 0 else default

stack = ConcurrentStack (size=1)

###############################################################################
###############################################################################

def sub_side (verbose: bool=False) -> None:

    curr_tick = None
    curr_tick_time = timedelta (0)
    curr_real_time = datetime.min

    for line in sys.stdin:

        last_tick = curr_tick
        last_real_time = curr_real_time
        last_tick_time = curr_tick_time

        curr_tick = JSON.decode (line.replace ("'", '"'))
        curr_tick_time = datetime.fromtimestamp (curr_tick['timestamp'])
        curr_real_time = datetime.now ()

        if last_tick:
            ## numerator: difference *measured* between ticks
            n = (curr_real_time - last_real_time).total_seconds ()
            ## denominator: difference *timestamped* between ticks
            d = (curr_tick_time - last_tick_time).total_seconds ()
            ## simulation acceleration factor: less is faster
            curr_siac = n / d; stack.put ((curr_tick, n / d))

            if verbose: print ('<%s> %s => %.6f' %
                (curr_tick_time, curr_tick, curr_siac), file=sys.stderr)

    stack.put ((curr_tick, 0.0))

def pub_side (interval: float, verbose: bool=False) -> None:

    curr_tick, curr_siac = None, sys.float_info.epsilon
    t0 = time.time ()

    while curr_siac > 0.0:
        last_tick, last_siac = curr_tick, curr_siac
        curr_tick, curr_siac = stack.top (default=(last_tick, last_siac))

        if curr_tick:
            if verbose: print ('[%s] %s' %
                (datetime.fromtimestamp (t0), curr_tick), file=sys.stderr)

            print (curr_tick, file=sys.stdout); sys.stdout.flush ()

        dt = interval * curr_siac - (time.time () - t0)
        if dt > 0.0: time.sleep (dt)
        t0 = time.time ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

    sub_thread = Thread (target=sub_side, args=[args.verbose])
    sub_thread.daemon = True
    pub_thread = Thread (target=pub_side, args=[args.interval, args.verbose])
    pub_thread.daemon = True

    sub_thread.start ()
    pub_thread.start ()

    try: pub_thread.join ()
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
