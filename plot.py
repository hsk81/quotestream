#!/usr/bin/env python2

###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import json as JSON
import argparse
import pylab
import sys

from datetime import datetime
from functools import reduce

###############################################################################
###############################################################################

def get_arguments (defaults=frozenset ({})):

    parser = argparse.ArgumentParser ()

    class attach (argparse.Action):
        """Appends values by *overwriting* initial defaults (if any)"""
        def __call__(self, parser, namespace, values, option_string=None):
            items = getattr (namespace, self.dest, [])
            if items == self.default:
                setattr (namespace, self.dest, [values])
            else:
                setattr (namespace, self.dest, list (items) + [values])

    parser.add_argument ('-v', '--verbose',
        default=False, action='store_true',
        help='verbose logging (default: %(default)s)')
    parser.add_argument ('-k', '--keep',
        default=False, action='store_true',
        help='keep plots (default: %(default)s)')
    parser.add_argument ("-n", "--ncols",
        default=1, type=int,
        help="number of columns (default: %(default)s [s])")
    parser.add_argument ('-c', '--colors', action=attach, nargs='+',
        default=defaults['colors'] if 'colors' in defaults else [],
        help='colors (default: %(default)s)')
    parser.add_argument ('-m', '--markers', action=attach, nargs='+',
        default=defaults['markers'] if 'markers' in defaults else [],
        help='markers (default: %(default)s)')
    parser.add_argument ('-w', '--widths', action=attach, nargs='+',
        default=defaults['widths'] if 'widths' in defaults else [],
        help='widths (default: %(default)s)')
    parser.add_argument ('-p', '--parameter-group', action=attach, nargs='+',
        default=defaults['parameter-group'] if 'parameter-group' in defaults else [],
        help='parameter group *per* result key (default: %(default)s)')

    return process (parser.parse_args ())

def process (args):

    args.parameter_group = list (map (lambda pg: list (
        filter (lambda p: p != "", pg)), args.parameter_group))
    args.colors = list (
        reduce (lambda a, b: a + b, args.colors, []))
    args.widths = list (
        reduce (lambda a, b: a + b, args.widths, []))
    args.markers = list (
        reduce (lambda a, b: a + b, args.markers, []))

    diff = len (args.parameter_group) - len (args.colors)
    args.colors += [args.colors[-1] for _ in range (diff)]
    diff = len (args.parameter_group) - len (args.widths)
    args.widths += [args.widths[-1] for _ in range (diff)]
    diff = len (args.parameter_group) - len (args.markers)
    args.markers += [args.markers[-1] for _ in range (diff)]

    return args

###############################################################################
###############################################################################

def loop (parameter_groups, colors, widths, markers, ncols, hold=False,
          verbose=False):

    values_matrix = []
    for parameter_group in parameter_groups:
        values_matrix.append ([[] for _ in parameter_group])

    for line in sys.stdin:
        tick = JSON.loads (line.replace ("'", '"'))

        for pg_index, parameter_group in enumerate (parameter_groups):

            def fn (value):
                if isinstance (value, list):
                    return value[0] if len (value) > 0 else None
                else:
                    return value

            for p_index, parameter in enumerate (parameter_group):
                values_matrix[pg_index][p_index].append (fn (tick[parameter]))

        if verbose:
            now = datetime.fromtimestamp (tick['timestamp'])
            print >> sys.stderr, '[%s] %s' % (now, tick)

        print >> sys.stdout, tick; sys.stdout.flush ()

    nrows = 1 if hold else len (values_matrix) / ncols
    ncols = 1 if hold else ncols

    for item in enumerate (zip (values_matrix, colors, widths, markers)):

        index, (values_group, color, width, marker) = item
        pylab.subplot (nrows, ncols, 1 if hold else (index + 1))
        pylab.plot (*values_group, color=color, linewidth=width, marker=marker)
        if not hold: pylab.grid ()

    if hold: pylab.grid ()
    pylab.show ()

###############################################################################
###############################################################################

if __name__ == "__main__":

    args = get_arguments (dict (
        colors=[['b', 'r', 'g', 'm', 'c', 'y']],
        markers=[['.']],
        widths=[[0]]
    ))

    try: loop (args.parameter_group, args.colors, args.widths, args.markers,
               args.ncols, hold=args.keep, verbose=args.verbose)

    except KeyboardInterrupt: pass

###############################################################################
###############################################################################
