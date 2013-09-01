#!/usr/bin/env python

###############################################################################
###############################################################################

from distutils.core import setup

###############################################################################
###############################################################################

setup(
    name='quotestream',
    version='0.0.2',
    license='GPLv3',
    author='Hasan Karahan',
    author_email='hasan.karahan81@gmail.com',
    url='https://bitbucket.org/hsk81/quotestream',
    description='Algorithmic Trading with Quote Stream',

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
