#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.reduce.do as do

###############################################################################
###############################################################################

class DiffCallable (object):

    def __init__ (self, n: int) -> None:
        self.n = n

    def __call__ (self, *arrays: [numpy.array], last=None) -> numpy.array:
        return numpy.array ([arr[0] - arr[self.n - 1] for arr in arrays])

    def __repr__ (self):
        return '@{0} - @{n-1}'

###############################################################################
###############################################################################

if __name__ == "__main__":
    diff = DiffCallable (n=2)

    parser = do.get_args_parser ({
        'stack-size': diff.n, 'function': diff, 'default': [], 'result': 'diff'
    })

    parser.description = \
        """
        Calculates the difference between two consecutive ticks by default, but
        it can also be used to calculate *overlapping* differences by
        increasing the *stack-size*.
        """

    parser.epilog = \
        """
        The difference is in general used to calculate a *return* at time
        t@{i}, r (t@{i}), and is defined as r (t@{i}) := r (Δt; t@{i}) =
        x (t@{i}) - x (t@{i}-Δt) where x (t@{i}) is a *homogeneous* sequence of
        logarithmic prices, and Δt is a time interval of fixed size.

        In the normal case, Δt is the interval of the homogeneous series, and
        r (t@{i}) is the series of the first differences of x (t@{i}). If the
        return is chosen to be a multiple of the series interval, the obtained
        intervals are *overlapping*.

        The return is usually a more suitable variable of analysis than the
        price, for several reasons. It is the variable of interest as a direct
        measure of the success of an investment. Further, the distribution of
        returns is more symmetric and stable over time than the distribution of
        prices. The return process is close to stationary whereas the price
        process is not.
        """

    args = do.get_args (parser=parser)
    diff.n = args.stack_size

    if isinstance (args.default, list):
        dsz = len (args.parameters) - len (args.default)
        for _ in range (dsz): args.default.append (0.0)

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
