#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import requests as req
import time
import zmq

from datetime import datetime

###############################################################################
###############################################################################

def get_ticker (url="https://www.bitstamp.net/api/ticker/"):

    res = req.get (url)
    assert res.status_code == 200
    return res

###############################################################################
###############################################################################

if __name__ == "__main__":

    last_ticker = None
    t0 = time.time ()
    dT = 1.250

    context = zmq.Context (1)
    socket = context.socket (zmq.PUB)
    socket.bind ("tcp://*:5556")

    while True:
        this_ticker = get_ticker ()

        if not last_ticker:
            json = this_ticker.json ()
            json['timestamp'] = datetime.now ().timestamp ()
            print ('TICK %s' % json)
            socket.send_json (json)

        else:
            if last_ticker.text != this_ticker.text:
                json = this_ticker.json ()
                json['timestamp'] = datetime.now ().timestamp ()
                print ('TICK %s' % json)
                socket.send_json (json)

        last_ticker = this_ticker
        dt = dT - (time.time () - t0)
        if dt > 0.000: time.sleep (dt)
        t0 = time.time ()

###############################################################################
###############################################################################
