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

class TakeCallable(object):

    def __init__(self, index=0, jndex=0):
        self.index = index
        self.jndex = jndex

    def __call__(self, *args: [numpy.array], last=None) -> numpy.array:
        return numpy.array([arg[self.jndex][self.index] for arg in args])

    def __repr__(self) -> str:
        return '@{0}[index]'

###############################################################################
###############################################################################

if __name__ == "__main__":
    take = TakeCallable(index=0, jndex=0)

    parser = do.get_args_parser({
        'function': take, 'result': '@[{index},{jndex}]'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    parser.add_argument("-i", "--index", default=take.index, type=int,
        help="1st index to take(default: %(default)s)")
    parser.add_argument("-j", "--jndex", default=take.index, type=int,
        help="2nd index to take(default: %(default)s)")

    args = do.get_args(parser=parser)
    take.index, take.jndex = args.index, args.jndex
    args.result = args.result.format(index=take.index, jndex=take.jndex)

    try: do.loop(args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
