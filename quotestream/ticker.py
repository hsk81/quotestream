#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import syslog
import requests as req
import time

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description=
        """
        Polls exchange for new ticks: The poll interval limits the maximum
        possible tick resolution, so keeping it as low as possible is
        desired. But since the exchange does impose a request limit per time
        unit it's not possible to poll beyond that cap - without getting
        banned.
        """)

    parser.add_argument('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging(default: %(default)s)')
    parser.add_argument('-i', '--interval',
        default=1.000, type=float,
        help='seconds between polls(default: %(default)s [s])')
    parser.add_argument('-c', '--currency-pair',
        default='btcusd', type=str,
        help='currency pair(default: %(default)s)')
    parser.add_argument('-u', '--url',
        default='https://www.bitstamp.net/api/v2/ticker/{0}/',
        help='JSON API(default: %(default)s)')

    return parser.parse_args()

def next_response(url: str) -> req.Response:

    try:
        res = req.get(url)
        return res if res.status_code == 200 else None

    except KeyboardInterrupt:
        raise

    except Exception as ex:
        print(ex, file=sys.stderr)
        syslog.syslog(syslog.LOG_ERR, str(ex))

def loop(
    interval: float, url: str, currency_pair: str, verbose: bool=False
) -> None:

    t0 = time.time()
    last_response = None

    try: url = url.format(currency_pair)
    except: pass

    while True:
        curr_response = next_response(url)
        if curr_response:
            if not last_response or last_response.text != curr_response.text:

                tick = curr_response.json()
                tick['timestamp'] = time.time()

                if verbose:
                    now = datetime.fromtimestamp(tick['timestamp'])
                    print('[%s] %s' %(now, tick), file=sys.stderr)

                print(tick, file=sys.stdout); sys.stdout.flush()
            last_response = curr_response

        dt = interval -(time.time() - t0)
        if dt > 0.000: time.sleep(dt)
        t0 = time.time()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments()
    try: loop(**vars(args))
    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
