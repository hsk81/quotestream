###############################################################################
###############################################################################

__author__ = 'hsk81'

###############################################################################
###############################################################################

import argparse

###############################################################################
###############################################################################

class attach(argparse.Action):
    """Appends values by *overwriting* initial defaults(if any)"""
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest, [])
        if items == self.default:
            setattr(namespace, self.dest, [values])
        else:
            setattr(namespace, self.dest, list(items) + [values])

###############################################################################
###############################################################################
