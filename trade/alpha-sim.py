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
        default=120.00, type=float,
        help="USD balance (default: %(default)s [USD])")

    parser.add_argument ("-f", "--fee",
        default=0.0050, type=float,
        help="Commission fee (default: %(default)s)")

    parser.add_argument ("-q", "--quota",
        default=0.0010, type=float,
        help="Per tick trading quota (default: %(default)s)")

    return parser.parse_args ()

def loop (btc, usd, fee, quota, verbose: bool=False) -> None:

    for line in sys.stdin:
        tick = JSON.loads (line.replace ('"', '"'))

        if tick['volatility'] > 1.0: ## trend (?)

            if tick['return'] > 0.0: ## upward trend (?)
                btc += quota * btc / tick['last'] * (1.0 - fee)
                usd -= quota * usd

            if tick['return'] < 0.0: ## downward trend (?)
                btc -= quota * btc
                usd += quota * btc * tick['last'] * (1.0 - fee)

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s: (btc:%.3f, usd:%.3f)' % (now, tick, btc, usd),
                file=sys.stderr)

        print ('%s: (btc:%s, usd:%s)' % (tick, btc, usd),
            file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = get_arguments ()

    try: loop (args.btc_balace, args.usd_balace, args.fee, args.quota,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
