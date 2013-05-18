#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import do
import numpy

###############################################################################
###############################################################################

class ReturnCallable (object):

    def __call__ (self, *args: list) -> numpy.array:
        return numpy.array (args[0]) - numpy.array (args[-2])

    def __repr__ (self):
        return '{0} - {n-1}'

###############################################################################
###############################################################################

if __name__ == "__main__":

    parser = do.get_args_parser ({
        'default': [[0.0]],
        'function': [[ReturnCallable ()]],
        'stack-size': [[600]], ## == 10 min., for 1 sec. interpolation
    })

    args = do.get_args (parser=parser)
    args = do.normalize (args)

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
