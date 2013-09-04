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

class EmaCallable (object):

    def __init__ (self, tau: float) -> None:
        self._tau = tau

    def __call__ (self, ts: numpy.array, *arrays: [numpy.array],
                  last: list=None) -> numpy.array:

        mu = numpy.exp ((ts[1] - ts[0]) / self.tau)
        nu = 1.0 - mu

        return numpy.array ([
            mu * el + nu * arr[0] for el, arr in zip (last, arrays)
        ])

    def __repr__ (self) -> str:
        return 'μ·EMA (t@{n-1}) + (1-μ)·z@{n-1} | ' \
               'μ := exp ((t@{n-1} - t@{n})/τ)'

    def get_tau (self) -> float:
        return self._tau

    def set_tau (self, value: float) -> None:
        self._tau = value

    tau = property (fget=get_tau, fset=set_tau)

###############################################################################
###############################################################################

if __name__ == "__main__":
    ema = EmaCallable (tau=600) ## 10mins

    parser = do.get_args_parser ({
        'stack-size': 2,
        'function': ema,
        'parameters': [['timestamp']],
        'result': 'ema'
    })

    parser.description = \
        """
        Calculates the *exponential moving average* EMA directly from an
        inhomogeneous time series: It requires two parameters where the first
        is fixed as *timestamp* and the second can be chosen freely.
        """

    parser.epilog =\
        """
        The basic EMA is a simple linear operator. It is an averaging operator
        with an exponentially decaying kernel: ema (t) = exp (-t/τ) / τ. The
        time interval τ it the time range over which the actual averaging takes
        place.

        The EMA is very important, because its computation is very efficient
        and other more complex operators can be built with it, such as moving
        averages (MAs), differentials, derivatives, and volatilities.

        The numerical evaluation is efficient because of the exponential form
        of the kernel, which leads to a simple iterative formula: EMA [τ;z] =
        μ·EMA (t@{n-1}) + (1-μ)·z@{n-1} with μ := exp ((t@{n-1} - t@{n})/τ).

        We have chosen here the *previous point* interpolation scheme and have
        omitted the *linear interpolation* and *next point* variations of the
        formula.
        """

    parser.add_argument ("-t", "--tau", default=ema.tau, type=float,
        help="time interval (default: %(default)s [s])")

    args = do.get_args (parser=parser)
    ema.tau = args.tau

    try: do.loop (args.function, args.parameters, args.stack_size,
        args.default, args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
