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

class VolatilityCallable (object):

    def __init__ (self, scale, p=2.0):

        self.scale = scale
        self.exponent = p

    def __call__ (self, *args: list) -> numpy.array:

        returns = args[:-1]
        size = len (returns)
        weights = [self.exponent] * size

        absolutes = numpy.absolute (returns)
        average = numpy.average (absolutes, weights=weights, axis=0) / size
        power = numpy.power (average, 1.0 / self.exponent)

        return power * self.scale

    def __repr__ (self): return '{0} - {n-1}'

###############################################################################
###############################################################################

if __name__ == "__main__":
    volatility = VolatilityCallable (scale=1.0)

    parser = do.get_args_parser ({
        'default': [[0.0]],
        'function': [[volatility]],
        'stack-size': [[600]], ## == 10 min., for 1 sec. interpolation
    })

    parser.add_argument ("-e", "--exponent", default=2.0, type=float,
        help="p-exponent (default: %(default)s)")
    parser.add_argument ("-s", "--scale", default=None, type=float,
        help="scaling factor (default: %(default)s)")

    args = do.get_args (parser=parser)
    args = do.normalize (args)

    volatility.exponent, volatility.scale = args.exponent, \
        numpy.sqrt (numpy.array (3600.0 * 24.0 * 365.0) / args.stack_size) \
            if args.scale is None else args.scale

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
