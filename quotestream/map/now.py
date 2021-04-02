#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.map.do as do
import time

###############################################################################
###############################################################################

class NowCallable(object):

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.array([time.time()])

    def __repr__(self) -> str:
        return '[time()]'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser({
        'function': NowCallable(),
        'parameters': [['timestamp']], ## required dummy!
        'result': 'now'
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
