#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.reduce.do as do

###############################################################################
###############################################################################

class VolatilityCallable(object):

    def __init__(self, scale, p=2.0):

        self.scale = scale
        self.exponent = p

    def __call__(self, *arrays: numpy.array, last=None) -> numpy.array:

        def vola(arr: numpy.array) -> float:

            absolutes = numpy.absolute(arr)
            powers = numpy.power(absolutes, self.exponent)
            average = numpy.average(powers, axis=0)
            power = numpy.power(average, 1.0 / self.exponent)

            return power * self.scale

        return numpy.array([vola(arr) for arr in arrays])

    def __repr__(self):

        return '⟨|@{0}|^p⟩^(1/p)'

###############################################################################
###############################################################################

if __name__ == "__main__":
    vola = VolatilityCallable(scale=1.0)

    parser = do.get_args_parser({
        'stack-size': 2, 'function': vola, 'result': 'vola'
    })

    ##
    ## `volatility.exponent`
    ## ---------------------
    ## A large exponent `p` gives more weight to the tails of the distribution.
    ## If `p` is too large, the realized volatility may have an asymptotically
    ## infinite expectation(if returns have a heavy-tailed density function.
    ##

    parser.add_argument("-e", "--exponent",
        default=2.0, type=float,
        help="p-exponent(default: %(default)s)")

    ##
    ## `volatility.scale`
    ## ------------------
    ## It is possible to get the volatility in *scaled* form: Although the
    ## volatility may be computed from e.g. 10-min returns, the expected vola-
    ## tility over another time interval(e.g. 1 hour or year) may also be
    ## calculated. Through a Gaussian scaling law, `v^2 <- dt`, the following
    ## definition of scaled volatility is obtained:
    ##
    ##     v_scaled = square-root {dt_scaled / dt} * v.
    ##

    parser.add_argument("-s", "--scale",
        default=None, type=float,
        help="scaling factor; overrides -i(default: %(default)s)")

    ##
    ## `volatility.interval-scaled`
    ## ----------------------------
    ## The most popular choice of the scaling reference interval `dt_scale` is
    ## 1 year. If this is chosen, then `v_scaled` is called an *annualized*
    ## volatility.
    ##

    parser.add_argument("-i", "--interval-scaled",
        default=3600.0 * 24.0 * 365.0, type=float,
        help="scaled interval(default: %(default)s [s])")

    args = do.get_args(parser=parser)

    vola.exponent, vola.scale = args.exponent, \
        numpy.sqrt(numpy.array(args.interval_scaled) / args.stack_size) \
            if args.scale is None else args.scale ## override `interval-scaled`

    try: do.loop(args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
