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

class Ema3Callable (object):

    def __init__ (self, tau: float) -> None:

        self._ema = emalib.EmaCallable (tau=tau)
        self._tau = tau

    def __call__ (self, ts: numpy.array, arr0: numpy.array, *_: [numpy.array],
                  last: list=None) -> numpy.array:

        ema1 = self._ema (ts, arr0, last=[last[0]])
        ema2 = self._ema (ts, ema1, last=[last[1]])
        ema3 = self._ema (ts, ema2, last=[last[2]])

        return numpy.array ([ema1, ema2, ema3])

    def __repr__ (self) -> str:
        return 'EMA[τ;EMA[τ,n=2;@{0}]] | EMA[τ,n=2;@{0}] := EMA[τ;EMA[τ;@{0}]]'

    def get_tau (self) -> float:
        return self._ema.tau

    def set_tau (self, value: float) -> None:
        self._ema.tau = value

    tau = property (fget=get_tau, fset=set_tau)

###############################################################################
###############################################################################

if __name__ == "__main__":
    ema = Ema3Callable (tau=600) ## 10mins

    parser = do.get_args_parser ({
        'stack-size': 2,
        'function': ema,
        'parameters': [['timestamp']],
        'default': [0.0, 0.0, 0.0],
        'result': 'ema-3'
    })

    parser.description = \
        """
        Calculates the *third* EMA directly from an inhomogeneous time series:
        It requires two parameters where the first is fixed as *timestamp* and
        the second can be chosen freely.
        """

    parser.epilog =\
        """
        Delivers results for the *first*, *second* and *third* EMA operators:
        This is a necessity since each EMA-3 operator needs to access the
        results of the previous EMA-1, EMA-2 *and* EMA-3 calculations!

        Contrary to the EMA-1 operator the implementation of EMA-3 considers
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
