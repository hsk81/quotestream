#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.interleave.do as do

###############################################################################
###############################################################################

class RatioCallable (object):

    def __call__ (self, *args: [numpy.array], last=None) -> numpy.array:

     ## if isnan (tick[result]):
     ##     tick[result] = list (
     ##         eval (default) if type (default) is str else default)
     ## if isposinf (tick[result]) or isneginf (tick[result]):
     ##     tick[result] = list (
     ##         eval (default) if type (default) is str else default)

        return numpy.divide (*args)

    def __repr__ (self) -> str:
        return 'divide (@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser ({
        'function': RatioCallable (), 'result': 'div'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args (parser=parser)

    try: do.loop (args.function, args.parameters, args.default, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
