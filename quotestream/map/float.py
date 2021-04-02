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

class FloatCallable(object):

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.array(args).astype(float)

    def __repr__(self) -> str:
        return 'array(@{0}).astype(float)'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser({
        'function': FloatCallable(), 'result': 'float'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args(parser=parser)

    if args.result == 'float':
        if len(args.parameters) > 0:
            args.result = args.parameters[0]

    try: do.loop(args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
