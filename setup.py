#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Gabriel Fernandes <gabrielfernndss@gmail.com>
# Héricles Emanuel <hericles.me@gmail.com>


try:
    from setuptools import setup
except ImportError:
    from os import system
    system('pip install --user setuptools')
    from setuptools import setup


setup(
   name='automated',
   version='1.2.0',
   description='Automatizador de tarefas - LEDA',
   license='MIT',
   classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
   url='https://github.com/gabrielfern/automated-leda-tasks',
   author='Gabriel Fernandes',
   author_email='gabrielfernndss@gmail.com',
   packages=['automated'],
   install_requires=['requests', 'python-crontab'],
)
