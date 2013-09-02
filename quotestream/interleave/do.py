#!/usr/bin/env python

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse
import sys
import ujson as JSON

from datetime import datetime
from functools import reduce
from numpy import *

###############################################################################
###############################################################################

def get_args (defaults: dict=frozenset ({}),
              parser: argparse.ArgumentParser=None) -> argparse.Namespace:

    return normalize (parser.parse_args () if parser
        else get_args_parser (defaults=defaults).parse_args ())

def get_args_parser (defaults: dict=frozenset ({})) -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser (description=
        """
        Generic interleaver: Applies a function to parameters, that do not all
        to be present in the current tick. In case of missing parameter values
        the most recent value is used - if possible; otherwise then the default
        result is returned.
        """, epilog=
        """
        The interleaver is useful when two sub-streams have been merged and the
        corresponding quotes do *not* share all attributes: By using the most
        recently seen value for missing attributes, a merge/calculation can be
        accomplished.
        """)

    parser.add_argument ("-v", "--verbose",
        default=False, action="store_true",
        help="verbose logging (default: %(default)s)")
    parser.add_argument ('-f', '--function',
        default=defaults['function'] if 'function' in defaults else 'array ([2.0])',
        help='reduction function (default: %(default)s)')
    parser.add_argument ('-p', '--parameters', action='append', nargs='+',
        default=defaults['parameters'] if 'parameters' in defaults else [],
        help='function parameter key(s) (default: %(default)s)')
    parser.add_argument ('-d', '--default',
        default=defaults['default'] if 'default' in defaults else [0.0],
        help='default result (default: %(default)s)')
    parser.add_argument ('-r', '--result',
        default=defaults['result'] if 'result' in defaults else 'result',
        help='result (default: %(default)s)')

    return parser

def normalize (args: argparse.Namespace) -> argparse.Namespace:
    args.parameters = reduce (lambda a, b: a + b, args.parameters, [])
    return args

###############################################################################
###############################################################################

def loop (function: str or callable, parameters: list, default: str or float,
          result: str, verbose: bool=False) -> None:

    tick, most_recent = None, {
        index: None for index, _ in enumerate (parameters)
    }

    for line in sys.stdin:
        last, tick = tick, JSON.decode (line.replace ("'", '"'))

        for index, p in enumerate (parameters):
            if p in tick: most_recent[index] = array (tick[p])

        values = most_recent.values ()
        interleaved = not any ([value is None for value in values])

        if interleaved:
            last_result = last[result] if last \
                else list (eval (default) if type (default) is str
                    else default)

            if callable (function):
                tick[result] = list (function (
                    *values, last=last_result
                ).flatten ())
            else:
                tick[result] = list (eval (function.format (last=last_result,
                    **{p: v for p, v in zip (parameters, values)}
                )).flatten ())
        else:
            tick[result] = list (eval (default) if type (default) is str
                else default)

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print ('[%s] %s' % (now, tick), file=sys.stderr)

        print (tick, file=sys.stdout); sys.stdout.flush ()

###############################################################################
###############################################################################

if __name__ == "__main__":
    args = get_args ()

    try: loop (args.function, args.parameters, args.default, args.result,
        verbose=args.verbose)

    except KeyboardInterrupt:
        pass

###############################################################################
###############################################################################
