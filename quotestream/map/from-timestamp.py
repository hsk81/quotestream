#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import datetime
import numpy
import quotestream.map.do as do

###############################################################################
###############################################################################

class FromTimestampCallable(object):

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.array(list(
            map(str, map(datetime.datetime.fromtimestamp, args))
        ))

    def __repr__(self) -> str:
        return 'map(str, map(from-timestamp(@{0}))'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser({
        'function': FromTimestampCallable(), 'result': '@'
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
