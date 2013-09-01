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

class ExpCallable (object):

    def __call__ (self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.exp (args)

    def __repr__ (self) -> str:
        return 'exp (@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser ({
        'function': ExpCallable (), 'result': 'exp'
    })

    parser.description = \
        """
        """

    parser.epilog =\
        """
        """

    args = do.get_args (parser=parser)

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
