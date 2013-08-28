#!/usr/bin/env python

###############################################################################
###############################################################################

from distutils.core import setup

###############################################################################
###############################################################################

setup(
    name='fx-bitstamp',
    version='0.0.1',
    license='GPLv3',
    author='Hasan Karahan',
    author_email='hasan.karahan81@gmail.com',
    url='https://bitbucket.org/hsk81/fx-bitstamp',
    description='Algorithmic trading on Bitstamp.net',

    requires=[
        'ipython>=1.0.0',
        'numpy>=1.7.1',
        'python-dateutil>=2.1',
        'pyzmq>=13.1.0',
        'requests>=1.2.3',
        'ujson>=1.33',
    ]
)

###############################################################################
###############################################################################
