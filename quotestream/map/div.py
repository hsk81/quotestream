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

    def __init__ (self, default):
        self.default = default

    def __call__ (self, *args: [numpy.array], last: list=None) -> numpy.array:
        result = numpy.divide (*args)

        if numpy.isposinf (result) or numpy.isneginf (result) or \
           numpy.isnan (result):

            result = numpy.array (eval (self.default)
                if type (self.default) is str else self.default)

        return result

    def __repr__ (self):
        return 'div (*@{0})'

###############################################################################
###############################################################################

if __name__ == "__main__":
    div = DivCallable (default=[1.0])

    parser = do.get_args_parser ({
        'function': div, 'default': div.default, 'result': 'div'
    })

    parser.description = \
        """
        """

    parser.epilog = \
        """
        """

    args = do.get_args (parser=parser)
    div.default = args.default

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
