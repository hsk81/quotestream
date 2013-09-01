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

class RatioCallable (object):

    def __init__ (self, default: list) -> None:
        self.default = numpy.array (default)

    def __call__ (self, lhs, rhs: numpy.array, last: list=None) -> numpy.array:
        quotient = lhs[0] / rhs[0]

        if numpy.isnan (quotient):
            quotient = self.default
        if numpy.isposinf (quotient) or numpy.isneginf (quotient):
            quotient = self.default

        return quotient

    def __repr__ (self):
        return '@{0}["numerator"] / @{0}["denominator"]'

###############################################################################
###############################################################################

if __name__ == "__main__":
    ratio = RatioCallable (default=[1.0])

    parser = do.get_args_parser ({
        'function': ratio, 'default': ratio.default, 'result': 'ratio'
    })

    args = do.get_args (parser=parser)
    ratio.default = args.default

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
