#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.reduce.do as do
import quotestream.reduce.ema as emalib

###############################################################################
###############################################################################

class Ema2Callable (object):

    def __init__ (self, tau: float) -> None:

        self.tau = tau
        self.ema = emalib.EmaCallable (tau=tau)

    def __call__ (self, ts: numpy.array, arr0: numpy.array, *_: [numpy.array],
                  last: list=None) -> numpy.array:

        ema1 = self.ema (ts, arr0, last=[last[0]])
        ema2 = self.ema (ts, ema1, last=[last[1]])

        return numpy.array ([ema1, ema2])

    def __repr__ (self) -> str:
        return 'μ·EMA (t@{n-1}) + (1-μ)·z@{n-1} | ' \
               'μ := exp ((t@{n-1} - t@{n})/τ)'

###############################################################################
###############################################################################

if __name__ == "__main__":
    ema = Ema2Callable (tau=600) ## 10mins

    parser = do.get_args_parser ({
        'stack-size': 2,
        'function': ema,
        'parameters': [['timestamp']],
        'default': [0.0, 0.0],
        'result': 'ema-2'
    })

    parser.description = \
        """
        Calculates the *second* EMA directly from an inhomogeneous time series:
        It requires two parameters where the first is fixed as *timestamp* and
        the second can be chosen freely.
        """

    parser.epilog =\
        """
        Delivers results for the *first* and *second* EMA operators: This is a
        necessity since each EMA-2 operator needs to access the results of the
        previous EMA-1 *and* EMA-2 calculations!

        Contrary to the EMA-1 operator the implementation of EMA-2 considers
        only a single extra parameter (in addition to `timestamp`).
        """

    parser.add_argument ("-t", "--tau", default=ema.tau,
        type=float, help="time interval (default: %(default)s [s])")

    args = do.get_args (parser=parser)
    ema.tau = args.tau

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
