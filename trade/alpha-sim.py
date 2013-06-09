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

    parser.add_argument ("-btc", "--btc-balance",
        default=1.0000, type=float,
        help="BTC balance (default: %(default)s [BTC])")

    parser.add_argument ("-usd", "--usd-balance",
        default=100.00, type=float,
        help="USD balance (default: %(default)s [USD])")

    parser.add_argument ("-f", "--fee",
        default=0.0050, type=float,
        help="Commission fee (default: %(default)s)")

    parser.add_argument ("-q", "--quota",
        default=0.0010, type=float,
        help="Per tick trading quota (default: %(default)s)")

    return parser.parse_args ()

def loop (btc, usd, fee, quota, verbose: bool=False) -> None:

    btc = array ([btc])
    usd = array ([usd])
    fee = array ([fee])

    ratio = array ([0.0])
    ret = array ([0.0])

    for line in sys.stdin:
        tick = JSON.loads (line.replace ("'", '"'))

        ratio = array (0.382 * ratio + 0.618 * array (tick['ratio']))
        ret = array (0.382 * ret + 0.618 * array (tick['return']))

        if ratio > 1.00: ## trend?

            if ret > 0.0: ## positive
                btc += quota * usd / tick['price'] * (1.0 - fee)
                usd -= quota * usd

            if ret < 0.0: ## negative
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

    try: loop (args.btc_balance, args.usd_balance, args.fee, args.quota,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
