#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

from reduce import get_arguments, loop

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments ({'stack-size': [[1]], 'function': [
        [lambda curr, prev: float (curr) * 0.618 + float (prev) * 0.382]
    ]})

    if not all (args.default):
        for index, (d, p) in enumerate (zip (args.default, args.parameter)):
            args.default[index] = p if d is None else d

    try: loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
