#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import time
import zmq

from datetime import datetime
from threading import Thread, Lock

###############################################################################
###############################################################################

def get_arguments ():

    parser = argparse.ArgumentParser (description=
        "Transforms an inhomogeneous time series to a homogeneous one by "
        "re-delivering the most recent tick in regular intervals.")

    parser.add_argument ("-s", "--silent",
        default=False, action="store_true",
        help="skip CLI logging (default: %(default)s)")
    parser.add_argument ("-sub", "--sub-address",
        default='tcp://127.0.0.1:8178',
        help="ticker subscription address (default: %(default)s)")
    parser.add_argument ("-pub", "--pub-address",
        default='tcp://*:7881',
        help="ticker publication address (default: %(default)s)")
    parser.add_argument ("-dT", "--pub-interval",
        default=1.000, type=float,
        help="publication interval (default: %(default)s [s])")

    return parser.parse_args ()

###############################################################################
###############################################################################

class Stack (object):

    def __init__ (self, size=0):

        self._lock = Lock ()
        self._list = []
        self._size = size

    def put (self, item):

        with self._lock:
            if self._size > 0:
                while len (self._list) >= self._size:
                    self._list.pop ()

            self._list.insert (0, item)

    def get (self, default=None):

        with self._lock:
            return self._list.pop (0) if len (self._list) > 0 else default

    def top (self, default=None):

        with self._lock:
            return self._list[0] if len (self._list) > 0 else default

ticks = Stack (size=2)

###############################################################################
###############################################################################

def sub_side (context, sub_address, silent):

    def loop (socket):

        while True:
            curr_tick = socket.recv_json ()
            ticks.put (curr_tick)
            if not silent: print ('[%s] %s' % (
                datetime.fromtimestamp (curr_tick['timestamp']), curr_tick))

    socket = context.socket (zmq.SUB)
    socket.connect (sub_address)
    socket.setsockopt_string (zmq.SUBSCRIBE, '')

    try: loop (socket)
    finally: socket.close ()

def pub_side (context, pub_address, interval, silent):

    def loop (socket):
        curr_tick = None
        t0 = time.time ()

        while True:
            last_tick = curr_tick
            curr_tick = ticks.top (default=last_tick)

            if curr_tick:
                socket.send_json (curr_tick)
                if not silent: print ('<%s> %s' % (datetime.now (), curr_tick))

            dt = interval - (time.time () - t0)
            if dt > 0.000: time.sleep (dt)
            t0 = time.time ()

    socket = context.socket (zmq.PUB)
    socket.bind (pub_address)

    try: loop (socket)
    finally: socket.close ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    context = zmq.Context (2)

    sub_thread = Thread (target=sub_side, args=[context, args.sub_address,
        args.silent])
    pub_thread = Thread (target=pub_side, args=[context, args.pub_address,
        args.interval, args.silent])

    sub_thread.daemon = True
    sub_thread.start ()
    pub_thread.daemon = True
    pub_thread.start ()

    try: pub_thread.join ()
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
