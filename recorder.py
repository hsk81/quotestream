#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import zmq

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments ():

    parser = argparse.ArgumentParser (description=
        "Records ticks to which it's subscribed to into a file. If previous "
        "records exists then the new ticks are appended at the end of the "
        "file.")

    parser.add_argument ("-s", "--silent",
        default=False, action="store_true",
        help="skip CLI logging (default: %(default)s)")
    parser.add_argument ("-sub", "--sub-address",
        default='tcp://127.0.0.1:8888',
        help="ticker subscription address (default: %(default)s)")
    parser.add_argument ("-f", "--filename",
        default='log/ticks.log',
        help="File to record to (default: %(default)s)")

    return parser.parse_args ()

def loop (socket, filename, silent=True):

    with open (filename, 'a') as file:

        while True:
            tick = socket.recv_json ()
            file.write (str (tick).replace ("'", '"') + '\n')
            file.flush ()

            if not silent:
                now = datetime.fromtimestamp (tick['timestamp'])
                print ('[%s] %s' % (now, tick))

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (1)

    socket = context.socket (zmq.SUB)
    socket.connect (args.sub_address)
    socket.setsockopt_string (zmq.SUBSCRIBE, '')

    try:
        loop (socket, args.filename, silent=args.silent)

    except KeyboardInterrupt: pass
    finally: socket.close ()

###############################################################################
###############################################################################
