#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import ujson as JSON
import argparse
import sys

from datetime import datetime
from numpy import *

###############################################################################
###############################################################################

def get_arguments () -> argparse.Namespace:
    parser = argparse.ArgumentParser ()

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')

    parser.add_argument ("-b", "--balance",
        default=100.00, type=float,
        help="initial balance (default: %(default)s [USD])")

    parser.add_argument ("-f", "--fee",
        default=0.0020, type=float,
        help="commission fee (default: %(default)s)")

    parser.add_argument ("-q", "--quota",
        default=0.0010, type=float,
        help="Per tick trading quota (default: %(default)s)")

    return parser.parse_args ()

def loop (balance, fee, quota, verbose: bool=False) -> None:

    line = sys.stdin.readline ()
    tick = JSON.loads (line.replace ("'", '"'))

    btc = 0.0 * balance / array (tick['price'])
    usd = 1.0 * balance * array ([1.000000000])
    fee = array ([fee])

    ratio = array ([0.0]) ## ratio of two volatility series of return
    ret = array ([0.0]) ## return of log-price

    for line in sys.stdin:
        tick = JSON.loads (line.replace ("'", '"'))

        ratio = array (0.382 * ratio + 0.618 * array (tick['ratio']))
        ret = array (0.382 * ret + 0.618 * array (tick['return']))

        if ratio > 1.75: ## trend

            if ret > 0.0: ## positive
                btc += quota * usd / tick['price'] * (1.0 - fee)
                usd -= quota * usd

            if ret < 0.0: ## negative
                usd += quota * btc * tick['price'] * (1.0 - fee)
                btc -= quota * btc

        elif ratio < 1.25: ## no trend

            if btc > 0.0: ## check balance
                usd += quota * btc * tick['price'] * (1.0 - fee)
                btc -= quota * btc

        tick['btc'], tick['usd'] = list (btc), list (usd)
        tick['tot'] = list (btc * tick['price'] + usd)

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = get_arguments ()

    try: loop (args.balance, args.fee, args.quota,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
