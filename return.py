#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import math
import zmq

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments ():

    parser = argparse.ArgumentParser (description=
        "Calculates the return of prices; by default the actual `last` price "
        "(of the most recent transaction) is used instead of the *calculated* "
        "`price` (based on the most recent bid/ask pair).")

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")

    parser.add_argument ("-k", "--key-name",
        default='last', choices=['last', 'price'],
        help="value to base the returns on (default: %(default)s)")

    return parser.parse_args ()

def loop (sub_socket, pub_socket, key_name, silent=True):

    curr_tick = None
    curr_value = 0.0

    while True:
        last_tick = curr_tick
        curr_tick = sub_socket.recv_json ()
        last_value = curr_value
        curr_value = curr_tick[key_name]

        if last_tick:

            tick = {
                'return': curr_value - last_value,
                'timestamp': curr_tick['timestamp']
            }

            pub_socket.send_json (tick)
            if not silent:
                now = datetime.fromtimestamp (tick['timestamp'])
                print ('[%s] %s' % (now, tick))

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

    try:
        loop (args.key_name, silent=args.silent)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
