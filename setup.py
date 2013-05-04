from distutils.core import setup

setup(
    name='bitstamp.net',
    version='0.0.1',

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
        'lib.python3.3.distutils', 'lib.python3.3.importlib',
    ],

    install_requires=[
        'pyzmq>=13.1.0',
        'requests>=1.2.0'
    ],

    url='http://blackhan.ch/bitstamp',
    license='GPL',
    author='hsk81',
    author_email='hasan.karahan81@gmail.com',
    description='An FX client trading BTC on http://bitstamp.net'
)
