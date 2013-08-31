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

    def __init__ (self, n: int) -> None:
        self.n = n

    def __call__ (self, values: numpy.array, last=None) -> numpy.array:
        return values[0] - values[self.n - 1]

    def __repr__ (self):
        return '@{0} - @{n-1}'

###############################################################################
###############################################################################

if __name__ == "__main__":
    diff = DiffCallable (n=2)

    parser = do.get_args_parser ({
        'stack-size': diff.n, 'function': diff, 'result': 'diff'
    })

    args = do.get_args (parser=parser)
    diff.n = args.stack_size

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################