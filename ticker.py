#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import requests as req
import argparse
import time
import sys

from datetime import datetime

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:

    parser = argparse.ArgumentParser (description=
        'Polls exchange for new ticks: The poll interval limits the maximum '
        'possible tick resolution, so keeping it as low as possible is '
        'desired. But since the exchange does impose a request limit per time '
        'unit it\'s not possible to poll beyond that cap (without getting '
        'banned).')

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')
    parser.add_argument ('-o', '--out-keys',
        default=['timestamp', 'bid', 'ask', 'price', 'high', 'low', 'volume'],
        nargs='+', help='output keys (default: %(default)s)')
    parser.add_argument ('-m', '--map-to', action='append',
        default=[('last', 'price')],
        nargs='+', help='output maps (default: %(default)s)')
    parser.add_argument ('-i', '--interval',
        default=1.250, type=float,
        help='seconds between polls (default: %(default)s [s])')
    parser.add_argument ('-u', '--url',
        default='https://www.bitstamp.net/api/ticker/',
        help='API (default: %(default)s)')

    return parser.parse_args ()

def next_response (url: str) -> req.Response:

    try: res = req.get (url); return res if res.status_code == 200 \
        else None

    except KeyboardInterrupt:
        raise

    except Exception as ex:
        print (ex, file=sys.stderr); return None

def loop (map_to: dict, out_keys: list, interval: float, url: str,
          verbose: bool=False) -> None:

    def mapped (key: str, maps: dict) -> str:
        return maps[key] if key in maps else key

    def select (tick: dict, maps: dict, keys: list=None) -> dict: return {
        mapped (k, maps=maps): v for k, v in tick.items ()
        if not keys or mapped (k, maps=maps) in keys
    }

    t0 = time.time ()
    last_response = None

    while True:
        curr_response = next_response (url)
        if curr_response:
            if not last_response or last_response.text != curr_response.text:

                inp_tick = curr_response.json ()
                inp_tick['timestamp'] = time.time ()
                out_tick = select (inp_tick, map_to, keys=out_keys)

                if verbose:
                    now = datetime.fromtimestamp (inp_tick['timestamp'])
                    print ('[%s] %s' % (now, inp_tick), file=sys.stderr)

                print (out_tick, file=sys.stdout); sys.stdout.flush ()
            last_response = curr_response

        dt = interval - (time.time () - t0)
        if dt > 0.000: time.sleep (dt)
        t0 = time.time ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ()
    args.map_to = dict (args.map_to)

    try: loop (
        args.map_to, args.out_keys,
        args.interval, args.url,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
