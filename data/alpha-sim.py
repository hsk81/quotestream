#!/usr/bin/env python2

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import json
import pylab
import argparse

###############################################################################
###############################################################################

parser = argparse.ArgumentParser ()
parser.add_argument ('-f', '--log-file', default='alpha-sim.log',
    help='log file to process (default: %(default)s)')

args = parser.parse_args ()

###############################################################################
###############################################################################

ls = open (args.log_file).readlines ()
ls = map (lambda l: l.replace ("'", '"'), ls)
ls = map (json.loads, ls)

price = map (lambda l: l['price'], ls)
last = map (lambda l: l['last'], ls) ## log-price
ret = map (lambda l: l['return'], ls)
volatility = map (lambda l: l['volatility'], ls)
ratio = map (lambda l: l['ratio'], ls)

tot = map (lambda l: l['tot'], ls)
btc = map (lambda l: l['btc'], ls)
usd = map (lambda l: l['usd'], ls)

###############################################################################
###############################################################################

pylab.subplot (411)
pylab.plot (last, 'b.')
pylab.plot (last, 'b-')
pylab.grid ()

pylab.subplot (412)
pylab.plot (ret, 'r.')
pylab.plot (ret, 'r-')
pylab.grid ()

pylab.subplot (413)
pylab.plot (volatility, 'g.')
pylab.plot (ratio, 'm.')
pylab.plot (ratio, 'm-')
pylab.plot (volatility, 'w-')
pylab.grid ()

pylab.subplot (414)
pylab.plot (tot, 'c.')
pylab.plot (tot, 'black')
pylab.grid ()

###############################################################################
###############################################################################

pylab.show ()

###############################################################################
###############################################################################
