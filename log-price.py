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
        "Calculates the logarithms for the last price, the bid/ask and the"
        "high/low pair.")

    parser.add_argument ("-s", "--silent",
        default=False, action="store_true",
        help="skip CLI logging (default: %(default)s)")
    parser.add_argument ("-sub", "--sub-address",
        default='tcp://127.0.0.1:7001',
        help="ticker subscription address (default: %(default)s)")
    parser.add_argument ("-pub", "--pub-address",
        default='tcp://*:7002',
        help="ticker publication address (default: %(default)s)")

    return parser.parse_args ()

def loop (sub_socket, pub_socket, silent=True):

    while True:
        sub_tick = sub_socket.recv_json ()

        ask, bid = float (sub_tick['ask']), float (sub_tick['bid'])
        high, low = float (sub_tick['high']), float (sub_tick['low'])
        last, volume = float (sub_tick['last']), float (sub_tick['volume'])

        log_price, log_last = math.log (math.sqrt (ask * bid)), math.log (last)
        log_ratio = (log_price - log_last) / log_last
        log_high, log_low = math.log (high), math.log (low)

        pub_tick = {
            'log-ratio': log_ratio,
            'log-price': log_price,
            'log-last': log_last,
            'log-high': log_high,
            'log-low': log_low,
            'volume': volume
        }

        pub_socket.send_json (pub_tick)

        if not silent:
            print ('[%s] %s' % (datetime.now (), pub_tick))

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (1)

    sub_socket = context.socket (zmq.SUB)
    sub_socket.connect (args.sub_address)
    sub_socket.setsockopt_string (zmq.SUBSCRIBE, '')
    pub_socket = context.socket (zmq.PUB)
    pub_socket.bind (args.pub_address)

    try:
        loop (sub_socket, pub_socket, silent=args.silent)

    except KeyboardInterrupt:
        pass

    finally:
        sub_socket.close ()
        pub_socket.close ()

###############################################################################
###############################################################################
