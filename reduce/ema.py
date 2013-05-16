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

    args = do.get_arguments ({'stack-size': [[1]], 'function': [
        [lambda curr, last: list (numpy.array (
            numpy.array (curr) * 0.618 + numpy.array (last) * 0.382))]
    ]})

    if not all (args.default):
        for index, (d, p) in enumerate (zip (args.default, args.parameter)):
            args.default[index] = p if d is None else d ## default is parameter

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
