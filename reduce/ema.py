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

class EmaCallable (object):

    def __init__ (self, tau: float) -> None:
        self._tau = tau

    def __call__ (self, ts, values: list, last: list) -> numpy.array:
        mu = numpy.exp ((ts[1] - ts[0]) / self.tau)
        return mu * last[0] + (1.0 - mu) * values[0]

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
        'stack-size': 2, 'function': ema
    })

    parser.add_argument ("-t", "--tau", default=ema.tau, type=float,
        help="Time interval (default: %(default)s [s])")

    args = do.get_args (parser=parser)
    ema.tau = args.tau

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
