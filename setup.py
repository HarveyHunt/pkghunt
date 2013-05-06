#!/usr/bin/python3
import os
import distribute_setup
# Install setuptools for the user.
distribute_setup.use_setuptools()
from setuptools import setup
from setuptools import find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='PkgHunt',
      packages = find_packages(),
      version='1.0',
      scripts=['pkghunt.py'],
      description='Download, install and manage software packages created from source code.',
      author='Harvey Hunt',
      author_email='harveyhuntnexus@gmail.com',
      license="BSD",
      keywords="package source code python3 c c++ install make pip github",
      long_description=read('README')
)
