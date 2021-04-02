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

class DiffCallable(object):

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.diff(numpy.array(args).flatten())

    def __repr__(self) -> str:
        return 'diff(@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser({
        'function': DiffCallable(), 'result': 'diff'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args(parser=parser)

    try: do.loop(args.function, args.parameters, args.default, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
