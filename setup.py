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

    packages=[
        'lib.python3.3.site-packages.distribute-0.6.34-py3.3.egg._markerlib',
        'lib.python3.3.site-packages.distribute-0.6.34-py3.3.egg.setuptools',
        'lib.python3.3.site-packages.distribute-0.6.34-py3.3.egg.setuptools.tests',
        'lib.python3.3.site-packages.distribute-0.6.34-py3.3.egg.setuptools.command',
        'lib.python3.3.site-packages.pip-1.3.1-py3.3.egg.pip',
        'lib.python3.3.site-packages.pip-1.3.1-py3.3.egg.pip.commands',
        'lib.python3.3.site-packages.pip-1.3.1-py3.3.egg.pip.vcs',
        'lib.python3.3.site-packages.pip-1.3.1-py3.3.egg.pip.backwardcompat',
        'lib.python3.3.collections', 'lib.python3.3.encodings',
        'lib.python3.3.distutils', 'lib.python3.3.importlib'
    ],

    requires=[
        'ipython',
        'requests',
        'python-dateutil',
        'pyzmq',
        'ujson',
    ]
)

###############################################################################
###############################################################################
