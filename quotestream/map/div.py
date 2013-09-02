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

class DivCallable (object):

    def __call__ (self, *args: [numpy.array], last: list=None) -> numpy.array:
        return numpy.divide (*args)

    def __repr__ (self):
        return 'div (*@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser ({
        'function': DivCallable (), 'result': 'div'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args (parser=parser)

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
