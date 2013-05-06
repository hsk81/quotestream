#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import requests as req
import argparse
import time
import zmq

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments ():

    parser = argparse.ArgumentParser (description=
        "Polls exchange for new ticks. The poll interval limits the maximum "
        "possible tick resolution, so keeping it as low as possible is "
        "desired. But since the exchange does impose a request limit per time "
        "unit it's not possible to poll beyond that cap (without getting "
        "banned). The ticks are published for further processing.")

    parser.add_argument ("-s", "--silent",
        default=False, action="store_true",
        help="skip CLI logging (default: %(default)s)")
    parser.add_argument ("-i", "--poll-interval",
        default=1.250, type=float,
        help="seconds between ticker polls (default: %(default)s [s])")
    parser.add_argument ("-pub", "--pub-address",
        default='tcp://*:8178',
        help="ticker publication address (default: %(default)s)")
    parser.add_argument ("-u", "--ticker-url",
        default='https://www.bitstamp.net/api/ticker/',
        help="API (default: %(default)s)")

    return parser.parse_args ()

def get_tick (url):

    res = req.get (url); return res if res.status_code == 200 else None

def loop (socket, poll_interval, ticker_url, silent=True):

    last_tick = None
    t0 = time.time ()

    while True:
        this_tick = get_tick (ticker_url)
        if this_tick:

            timestamp = time.time ()
            now = datetime.fromtimestamp (timestamp)
            if not last_tick or last_tick.text != this_tick.text:

                tick = this_tick.json ()
                if not silent: print ('[%s] %s' % (now, tick))
                tick['timestamp'] = timestamp
                socket.send_json (tick)

            last_tick = this_tick

        dt = poll_interval - (time.time () - t0)
        if dt > 0.000: time.sleep (dt)
        t0 = time.time ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()

    context = zmq.Context (1)
    socket = context.socket (zmq.PUB)
    socket.bind (args.pub_address)

    try:
        loop (socket, args.poll_interval, args.ticker_url, silent=args.silent)

    except KeyboardInterrupt:
        pass

    finally:
        socket.close ()

###############################################################################
###############################################################################
