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

class EmaIteratedCallable (object):

    def __init__ (self, tau: float, n: int) -> None:

        self.tau = tau
        self.n = n

    def __call__ (self, ts: numpy.array, array: numpy.array, *_: [numpy.array],
                  last: list=None) -> numpy.array:

        ema_last = array
        ema_list = []

        for index in range (self._n):
            ema_next = self.ema_callable (ts, ema_last, last=[last[index]])
            ema_list.append (ema_next)
            ema_last = ema_next

        return numpy.array (ema_list)

    def __repr__ (self) -> str:
        return 'EMA[τ;EMA[τ,n;@{0}]] | EMA[τ,n;@{0}] := EMA[τ;EMA[τ,n-1;@{0}]]'

    def get_tau (self) -> float:
        return self._tau
    def set_tau (self, value: float) -> None:
        self._ema_callable = None ## invalidate
        self._tau = value

    tau = property (fget=get_tau, fset=set_tau)

    def get_n (self) -> int:
        return self._n
    def set_n (self, value: int) -> None:
        self._n = value

    n = property (fget=get_n, fset=set_n)

    def get_ema_callable (self) -> emalib.EmaCallable:

        if self._ema_callable is None:
            self._ema_callable = emalib.EmaCallable (tau=self.tau)

        return self._ema_callable

    ema_callable = property (fget=get_ema_callable)

###############################################################################
###############################################################################

if __name__ == "__main__":
    ema_iterated = EmaIteratedCallable (tau=600, n=1) ## 10mins, no iteration

    parser = do.get_args_parser ({
        'stack-size': 2,
        'function': ema_iterated,
        'parameters': [['timestamp']],
        'default': [],
        'result': 'ema-{n}'
    })

    parser.description = \
        """
        Calculates the *n-th* EMA directly from an inhomogeneous time series:
        It requires two parameters where the first is fixed as `timestamp` and
        the second can be chosen freely.
        """

    parser.epilog =\
        """
        Delivers results for the *first* to *n-th* EMA operators: This is a
        necessity since each EMA-i operator needs to access the results of the
        previous EMA calculations!

        Contrary to the regular EMA operator the implementation of EMA-i does
        *not* considers any extra parameters except the first (in addition to
        `timestamp`).
        """

    parser.add_argument ("-t", "--tau", default=ema_iterated.tau,
        type=float, help="time interval (default: %(default)s [s])")
    parser.add_argument ("-i", "--iterations", default=ema_iterated.n,
        type=int, help="EMA iterations (default: %(default)s)")

    args = do.get_args (parser=parser)
    if isinstance (args.default, list): args.default = [0.0] * args.iterations
    args.result = args.result.format (n=args.iterations)

    ema_iterated.tau = args.tau
    ema_iterated.n = args.iterations

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
