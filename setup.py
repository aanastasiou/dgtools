import sys

from setuptools import setup, find_packages

setup(
    name='dgtools',
    version='1.0.0',
    description='An assembler and simulation toolchain for the Digirule2 series of hardware.',
    long_description=open('README.md').read(),
    author='Athanasios Anastasiou',
    author_email='athanastasiou@gmail.com',
    zip_safe=True,
    url='https://github.com/aanastasiou/dgtools',
    license='Apache2.0',
    packages=find_packages(),
    scripts=['dgtools/dgasm.py', 'dgtools/dgsim.py', 'dgtools/dginspect.py', 'dgtools/dgui.py'],
    install_requires=['click', 'pyparsing', 'urwid'])
