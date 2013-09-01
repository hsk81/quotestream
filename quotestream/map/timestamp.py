#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import datetime as dt
import numpy
import quotestream.map.do as do

###############################################################################
###############################################################################

class FromTimestampCallable (object):

    def __call__ (self, *args: list) -> numpy.array:
        return numpy.array (list (
            map (str, map (dt.datetime.fromtimestamp, args))
        ))

    def __repr__ (self) -> str:

        return 'map (str, map (from-timestamp (@{0}))'

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = do.get_arguments ({
        'function': FromTimestampCallable (),
        'parameters': [['timestamp']],
        'result': '@timestamp'
    })

    try: do.loop (args.function, args.parameters, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
