from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
   name='automated',
   version='1.0.0',
   description='A automated module',
   long_description=long_description,
   license='MIT',
   python_requires='>=3',
   url='https://github.com/gabrielfern/automated-leda-tasks',
   author='Gabriel Fernandes',
   author_email='gabrielfernndss@gmail.com',
   packages=['automated'],
   install_requires=['requests'],
)
