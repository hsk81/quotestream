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

class DiffCallable (object):

    def __call__ (self, curr: list, prev: list, *args: list) -> numpy.array:
        return numpy.array (numpy.array (curr) - numpy.array (prev))

    def __repr__ (self): return '{0} - {1}'

###############################################################################
###############################################################################

if __name__ == "__main__":
    diff = DiffCallable ()

    parser = do.get_args_parser ({
        'stack-size': [[2]], 'function': [[diff]], 'default': [[0.0]]
    })

    args = do.get_args (parser=parser)
    args = do.normalize (args)

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
