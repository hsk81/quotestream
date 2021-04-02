#!/usr/bin/env python

###############################################################################
###############################################################################

from setuptools import setup

###############################################################################
###############################################################################

setup(
    name='quotestream',
    version='0.0.3',
    license='GPLv3',
    author='Hasan Karahan',
    author_email='hasan.karahan@blackhan.com',
    url='https://github.com/hsk81/quotestream',
    description='Algorithmic Trading with Quotestream',
    install_requires=[
        'ipython>=7.22.0',
        'numpy>=1.20.2',
        'python-dateutil>=2.8.1',
        'pyzmq>=22.0.3',
        'requests>=2.25.1',
        'ujson>=4.0.2',
    ]
)

###############################################################################
###############################################################################
