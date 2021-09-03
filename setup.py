#!/usr/bin/env python
import os

with open(os.path.join('loglab', 'version.py'), 'rt') as f:
    version = f.read().strip()
    version = version.split('=')[1].strip('"')

__version__ = version

from distutils.core import setup

SCRIPTS = ['bin/loglab']
if os.name == 'nt':
    SCRIPTS += ['bin/loglab.bat']

setup(
    name='loglab',
    version=__version__,
    author="JeongJu Kim",
    author_email='haje01@gmail.com',
    url="https://github.com/haje01/loglab",
    description="Log format design and validate tool",
    platforms=["any"],
    packages=['loglab'],
    scripts=SCRIPTS,
    license=['MIT License'],
    install_requires=[
        'click',
        'pyyaml',
        'tabulate',
    ],
    extras_require={
        'dev': [
            'pytest',
            'coverage',
            'pyinstaller',
            'tox',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
    ]
)
