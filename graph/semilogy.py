#!/usr/bin/env python2

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

from __init__ import get_defaults
from __init__ import get_arguments
from __init__ import loop

import pylab

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments (get_defaults ())

    try:
        loop (args.parameter_group,
              args.colors,
              args.widths,
              args.markers,
              args.ncols,
              plotter=pylab.semilogy,
              hold=args.keep,
              verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
