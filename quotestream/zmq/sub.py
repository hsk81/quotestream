#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import ujson as JSON
import zmq

from datetime import datetime
from functools import reduce
from quotestream.util import attach

###############################################################################
###############################################################################

def get_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description=
        """
        Subscribes to a quote stream at an address. The following two protocols
        are supported: TCP and IPC.
        """, epilog=
        """
        The TCP protocol is meant for *inter* device communication and uses
        addresses of the form `tcp://IP:PORT` where the IP is required to be a
        concrete address - like 127.0.0.1 - to subscribe to; the PORT needs to
        be the same like the port of the publisher.

        For *intra* device communication the IPC protocol should be applied:
        The address has the `ipc:///PATH/TO/SOCKET` form, where the path should
        be a path to the UNIX socket of the publisher.
        """)

    parser.add_argument("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging(default: %(default)s)")
    parser.add_argument('-a', '--sub-address',
        default=[['tcp://127.0.0.1:8888']], action=attach, nargs='+',
        help='subscription address(default: %(default)s)')

    return parser.parse_args()

###############################################################################
###############################################################################

def loop(context: zmq.Context, addresses: list, verbose: bool=False) -> None:

    socket = context.socket(zmq.SUB)
    for address in addresses: socket.connect(address)
    socket.LINGER = 0

    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    line = socket.recv_string()

    while line != '\0':
        tick = JSON.decode(line.replace("'", '"'))

        if verbose:
            now = datetime.fromtimestamp(tick['timestamp'])
            print('[%s] %s' %(now, tick), file=sys.stderr)

        print(tick, file=sys.stdout); sys.stdout.flush()
        line = socket.recv_string()

###############################################################################
###############################################################################

def normalize(args: argparse.Namespace) -> argparse.Namespace:

    args.sub_address = list(reduce(lambda a, b: a + b, args.sub_address, []))
    return args

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = normalize(get_arguments())
    context = zmq.Context(1)

    try:
        loop(context, args.sub_address, verbose=args.verbose)
    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
