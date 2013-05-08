#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import json as JSON
import argparse
import time
import zmq

from dateutil import parser
from datetime import datetime

###############################################################################
###############################################################################

def get_arguments ():

    parser = argparse.ArgumentParser (description=
        "Publishes recorded ticks for simulation and training purposes with "
        "the possibility to adjust the tick speed as desired.")

    parser.add_argument ("-s", "--silent",
        default=False, action="store_true",
        help="skip CLI logging (default: %(default)s)")
    parser.add_argument ("-f", "--filename",
        default='log/ticks.log',
        help="file to read records from (default: %(default)s)")
    parser.add_argument ("-b", "--from-date",
        default=None,
        help="date to begin from (default: %(default)s)")
    parser.add_argument ("-e", "--to-date",
        default=None,
        help="date to stop at (default: %(default)s)")
    parser.add_argument ("-a", "--acceleration",
        default=1.000, type=float,
        help="time acceleration factor (default: %(default)s)")
    parser.add_argument ("-pub", "--pub-address",
        default='tcp://*:7000',
        help="ticker publication address (default: %(default)s)")

    return parser.parse_args ()

def loop (socket, filename, from_date, to_date, acceleration, silent=True):

    from_date = parser.parse (from_date) if from_date else None
    to_date = parser.parse (to_date) if to_date else None

    with open (filename, 'r') as file:

        curr_time = None
        for line in file:

            last_time = curr_time
            curr_tick = JSON.loads (line)
            curr_time = datetime.fromtimestamp (curr_tick['timestamp'])

            if from_date and from_date > curr_time: continue
            if to_date and to_date <= curr_time: break

            if last_time is not None:
                diff_secs = curr_time.timestamp () - last_time.timestamp ()
                time.sleep (diff_secs * acceleration)

            socket.send_string (line)
            if not silent: print ('[%s] %s' % (curr_time, curr_tick))

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (1)
    socket = context.socket (zmq.PUB)
    socket.bind (args.pub_address)

    try:
        loop (socket, args.filename, args.from_date, args.to_date,
              args.acceleration, silent=args.silent)

    except KeyboardInterrupt: pass
    finally: socket.close ()

###############################################################################
###############################################################################
