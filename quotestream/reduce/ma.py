#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.reduce.do as do
import quotestream.reduce.emai as emai

###############################################################################
###############################################################################

class MovingAverageCallable(object):

    def __init__(self, tau: float, n: int) -> None:

        self.tau = tau
        self.n = n

    def __call__(self, ts: numpy.array, array: numpy.array, *_: [numpy.array],
                  last: list=None) -> numpy.array:

        ema = self.ema_callable(ts, array, last=last).flatten()
        return numpy.array(ema.tolist() + [numpy.average(ema)])

    def __repr__(self) -> str:
        return "⟨EMA[τ';k]|k in [1,n]⟩ | τ' := 2τ/(n+1)"

    def get_tau(self) -> float:
        return self._tau
    def set_tau(self, value: float) -> None:
        self._ema_callable = None ## invalidate
        self._tau = value

    tau = property(fget=get_tau, fset=set_tau)

    def get_tau_prime(self) -> float:
        return 2.0 * self.tau /(self.n + 1.0)

    tau_prime = property(fget=get_tau_prime)

    def get_n(self) -> int:
        return self._n
    def set_n(self, value: int) -> None:
        self._ema_callable = None ## invalidate
        self._n = value

    n = property(fget=get_n, fset=set_n)

    def get_ema_callable(self) -> emai.EmaIteratedCallable:

        if self._ema_callable is None: self._ema_callable = \
            emai.EmaIteratedCallable(tau=self.tau_prime, n=self.n)

        return self._ema_callable

    ema_callable = property(fget=get_ema_callable)

###############################################################################
###############################################################################

if __name__ == "__main__":
    ma = MovingAverageCallable(tau=600, n=1) ## 10mins, no iteration

    parser = do.get_args_parser({
        'stack-size': 2,
        'function': ma,
        'parameters': [['timestamp']],
        'default': [],
        'result': 'ma-{n}'
    })

    parser.description = \
        """
        Calculates the *n-th* MA directly from an inhomogeneous time series:
        It requires two parameters where the first is fixed as `timestamp` and
        the second can be chosen freely.
        """

    parser.epilog =\
        """
        Delivers results for the *first* to *n-th* EMA operators, **plus** the
        MA as the last element: This is a necessity since each EMA-i operator
        needs to access the results of the previous EMA calculations, and since
        MA requires access to each EMA-i!
        """

    parser.add_argument("-t", "--tau", default=ma.tau,
        type=float, help="time interval(default: %(default)s [s])")
    parser.add_argument("-i", "--iterations", default=ma.n,
        type=int, help="MA iterations(default: %(default)s)")

    args = do.get_args(parser=parser)
    if isinstance(args.default, list):
        args.default = [0.0] *(args.iterations + 1)
    args.result = args.result.format(n=args.iterations)

    ma.tau = args.tau
    ma.n = args.iterations

    try: do.loop(args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
