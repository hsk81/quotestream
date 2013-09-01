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

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        """
        Pushes a quote stream at an address. The following two protocols are
        available: TCP and IPC.
        """, epilog=
        """
        The TCP protocol is meant for *inter* device communication and uses
        addresses of the form `tcp://IP:PORT` where an IP of `*` means that any
        subscriber from any IP address can subscribe to; the PORT can be any
        available port number.

        For *intra* device communication the IPC protocol should be applied:
        The address has the `ipc:///PATH/TO/SOCKET` form, where the path can be
        any arbitrary path to a UNIX socket.
        """)

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-a', '--pub-address',
        default='tcp://*:8888',
        help='publication address (default: %(default)s)')

    return parser.parse_args ()

###############################################################################
###############################################################################

def loop (context: zmq.Context, address: str, verbose: bool=False) -> None:

    socket = context.socket (zmq.PUSH)
    socket.bind (address)
    socket.LINGER = 0

    try:
        for line in sys.stdin:
            tick = JSON.decode (line.replace ("'", '"'))

            if verbose:
                now = datetime.fromtimestamp (tick['timestamp'])
                print ('[%s] %s' % (now, tick), file=sys.stderr)

            print (tick, file=sys.stdout); sys.stdout.flush ()
            socket.send_string (line)
    finally:
        socket.send_string ('\0')

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (1)

    try:
        loop (context, args.pub_address, verbose=args.verbose)
    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
