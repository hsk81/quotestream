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

    def __init__ (self, decay: float) -> None:
        self._decay_curr, self._decay_last = decay, 1.0 - decay

    def __call__ (self, curr: list, last: list, *args: list) -> numpy.array:
        curr = numpy.array (curr) * self._decay_curr
        last = numpy.array (last) * self._decay_last
        return numpy.array (curr + last)

    def __repr__ (self) -> str: return '{0}*%0.3f + {1}*%0.3f' % (
        self._decay_curr, self._decay_last)

    def get_decay (self) -> float:
        return self._decay_curr

    def set_decay (self, value: float) -> None:
        self._decay_curr, self._decay_last = value, 1.0 - value

    decay = property (fget=get_decay, fset=set_decay)

###############################################################################
###############################################################################

if __name__ == "__main__":
    ema = EmaCallable (decay=0.618)

    parser = do.get_args_parser ({
        'stack-size': [[1]], 'function': [[ema]]
    })

    parser.add_argument ("-w", "--ema-decay", default=ema.decay, type=float,
        help="Decay in [0.0/infinite, 1.0/no memory] (default: %(default)s)")

    parser.description = \
        """
        Calculates the exponential moving average (EMA) of a time series; the
        actual function applied by default is `current-value * 0.618 +
        last-value * 0.382`, where the EMA decay can be set to another value
        than the golden ratio of `0.618`.

        The time series of interest can be selected by using the `parameter`
        option and the name of the calculated series can be set using the
        `result` option. The `default` option is set internally to whatever
        `parameter` has been set to, to minimize build-up time for correct EMA
        values, but it can also be set to e.g. `0.0`.
        """

    args = do.get_args (parser=parser)
    args = do.normalize (args)
    ema.set_decay (args.ema_decay)

    if not all (args.default):
        for index, (d, p) in enumerate (zip (args.default, args.parameter)):
            args.default[index] = p if d is None else d ## default is parameter

    try: do.loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
