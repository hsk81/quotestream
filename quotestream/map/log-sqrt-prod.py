#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import numpy
import quotestream.map.do as do

###############################################################################
###############################################################################

class LogSqrtProdCallable (object):

    def __call__ (self, *args: list) -> numpy.array:
        return numpy.log (numpy.sqrt (numpy.prod (args)))

    def __repr__ (self) -> str:
        return 'log (sqrt (prod (@{0})))'

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = do.get_arguments ({
        'function': LogSqrtProdCallable (), 'result': 'log-sqrt-prod'
    })

    try: do.loop (args.function, args.parameters, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################