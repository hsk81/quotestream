#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import do
import numpy

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = do.get_arguments ({'stack-size': [[2]], 'function': [
        [lambda curr, prev, last: list (numpy.array (
            numpy.array (curr) * 1.000 - numpy.array (prev) * 1.000))]
    ]})

    if not all (args.default):
        for index, (d, p) in enumerate (zip (args.default, args.parameter)):
            args.default[index] = 0.0 if d is None else d ## default is 0.0

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
