#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import zmq
import sys

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser ()

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-sub', '--sub-address',
        default='tcp://127.0.0.1:8888',
        help='subscription address (default: %(default)s)')

    return parser.parse_args ()

###############################################################################
###############################################################################

def loop (context: zmq.Context, address: str, verbose: bool=False) -> None:

    socket = context.socket (zmq.SUB)
    socket.connect (address)
    socket.LINGER = 0

    socket.setsockopt_string (zmq.SUBSCRIBE, '')
    line = socket.recv_string ()

    while line != '\0':
        tick = JSON.decode (line.replace ("'", '"'))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()
        line = socket.recv_string ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (1)

    try: loop (context, args.sub_address, verbose=args.verbose)
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
