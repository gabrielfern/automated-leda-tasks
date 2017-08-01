#!/usr/bin/python
# Gabriel Fernandes <gabrielfernndss@gmail.com>

from setuptools import setup
from os import path


here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()


setup(
   name='automated',
   version='1.1.1',
   description='A automated package',
   long_description=long_description,
   license='MIT',
   classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
   url='https://github.com/gabrielfern/automated-leda-tasks',
   author='Gabriel Fernandes',
   author_email='gabrielfernndss@gmail.com',
   packages=['automated'],
   install_requires=['requests'],
)
