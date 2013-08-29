#!/usr/bin/env python2

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import json
import pylab
import argparse

from numpy import array

###############################################################################
###############################################################################

parser = argparse.ArgumentParser ()

parser.add_argument ('-f', '--log-file', default='alpha-sim.log',
                     help='log file to process (default: %(default)s)')
parser.add_argument ('-max', '--max-percent', default=100.0, type=float,
                     help='maximum position percent (default: %(default)s)')
parser.add_argument ('-min', '--min-percent', default=0.000, type=float,
                     help='minimum position percent (default: %(default)s)')

args = parser.parse_args ()

###############################################################################
###############################################################################

ls = open (args.log_file).readlines ()
max_position = int (len (ls) * args.max_percent / 100.0)
min_position = int (len (ls) * args.min_percent / 100.0)
ls = ls[min_position:max_position]

ls = list (map (lambda l: l.replace ("'", '"'), ls))
ls = list (map (json.loads, ls))

price = array (map (lambda l: l['price'], ls))
last = array (map (lambda l: l['last'], ls)) ## log-price
ret = array (map (lambda l: l['return'], ls))
volatility = array (map (lambda l: l['volatility'], ls))
ratio = array (map (lambda l: l['ratio'], ls))

tot = array (map (lambda l: l['tot'], ls))
btc = array (map (lambda l: l['btc'], ls))
usd = array (map (lambda l: l['usd'], ls))

###############################################################################
###############################################################################

pylab.subplot (321)
pylab.plot (price, 'b.')
pylab.plot (price, 'b-')
pylab.grid ()

pylab.subplot (323)
pylab.plot (tot - tot[0], 'c.')
pylab.plot (tot - tot[0], 'black')
pylab.grid ()

pylab.subplot (325)
pylab.plot (usd, 'm.')
pylab.plot (usd, 'black')
pylab.plot (btc * price, 'y.')
pylab.plot (btc * price, 'black')
pylab.grid ()

pylab.subplot (322)
pylab.plot (ret, 'r.')
pylab.plot (ret, 'r-')
pylab.grid ()

pylab.subplot (324)
pylab.plot (ratio, 'm.')
pylab.plot (ratio, 'black')
pylab.grid ()

pylab.subplot (326)
pylab.plot (volatility, 'g.')
pylab.plot (volatility, 'black')
pylab.grid ()

###############################################################################
###############################################################################

pylab.show ()

###############################################################################
###############################################################################
