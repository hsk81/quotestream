#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.map.do as do

###############################################################################
###############################################################################

class ProdCallable(object):

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.prod(args)

    def __repr__(self) -> str:
        return 'prod(@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser({
        'function': ProdCallable(), 'result': 'prod'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args(parser=parser)

    try: do.loop(args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
