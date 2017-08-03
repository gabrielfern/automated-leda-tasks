#!/usr/bin/python
# Gabriel Fernandes <gabrielfernndss@gmail.com>

from setuptools import setup


setup(
   name='automated',
   version='1.1.4',
   description='A automated package',
   long_description=open('README.md').read(),
   license='MIT',
   classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
   url='https://github.com/gabrielfern/automated-leda-tasks',
   author='Gabriel Fernandes',
   author_email='gabrielfernndss@gmail.com',
   packages=['automated'],
   install_requires=['requests', 'setuptools'],
   data_files=[('README.md', ['README.md']),]
)
