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

    args = get_arguments ({
        'stack-size': [[2]], 'function': [
            [lambda curr, prev, *rest: float (curr) - float (prev)]
        ]
    })

    if not all (args.default):
        for index, (d, p) in enumerate (zip (args.default, args.parameter)):
            args.default[index] = 0.0 if d is None else d

    try: loop (args.function, args.parameter, args.stack_size, args.default,
        args.result, verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
