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

    parser = argparse.ArgumentParser ()
    parser.add_argument("-p", "--poll-interval",
        default=1.250, type=float,
        help="seconds between ticker polls (default: %(default)s [s])")
    parser.add_argument("-a", "--pub-address",
        default='tcp://*:8178',
        help="ticker publication address (default: %(default)s)")
    parser.add_argument("-u", "--ticker-url",
        default='https://www.bitstamp.net/api/ticker/',
        help="API (default: %(default)s)")

    return parser.parse_args ()

def get_ticker (url):

    res = req.get (url)
    assert res.status_code == 200
    return res

def loop (poll_interval, ticker_url):

    last_ticker = None
    t0 = time.time ()

    while True:
        this_ticker = get_ticker (ticker_url)
        now = datetime.now ()

        if not last_ticker or last_ticker.text != this_ticker.text:

            json = this_ticker.json ()
            print ('[%s] %s' % (now, json))
            json['timestamp'] = now.timestamp ()
            socket.send_json (json)

        last_ticker = this_ticker
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
        loop (args.poll_interval, args.ticker_url)

    except KeyboardInterrupt:
        pass

    finally:
        socket.close ()

###############################################################################
###############################################################################
