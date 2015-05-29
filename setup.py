#! /usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

def read(fname):
    return open (os.path.join(os.path.dirname(__file_), fname)).read()

setup(
    name = 'c2c',
    version = '0.7',
    description = 'A python web server that connects to the Asterisk AMI',
    url = 'https://github.com/TheSeanBrady/c2c.git',
    author = 'Sean Brady',
    author_email = 'sbrady@haikuengineering.com',
    license = 'UNLICENSE',

    classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Asterisk Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: UNLICENSE',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    install_requires = [
        'pyst2',
        'web.py'
    ],
)

