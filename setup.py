import sys

from setuptools import setup, find_packages

setup(
    name='dgtools',
    version='1.0.1',
    description='An assembler and simulation toolchain for the Digirule2 series of hardware.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Athanasios Anastasiou',
    author_email='athanastasiou@gmail.com',
    zip_safe=True,
    url='https://github.com/aanastasiou/dgtools',
    license='Apache2.0',
    packages=find_packages(),
    scripts=['dgtools/dgasm.py', 'dgtools/dgsim.py', 'dgtools/dginspect.py', 'dgtools/dgui.py', 'dgtools/dgform.py'],
    package_data={'dgtools':['css_themes/*.css']},
    install_requires=['click', 'pyparsing', 'urwid', 'pygments', 'intelhex'],
    python_requires='>=3.6',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Education',
                 'Intended Audience :: Information Technology',
                 'Natural Language :: English',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Assemblers',
                 'Topic :: Software Development :: Code Generators',
                 'Topic :: Software Development :: Compilers',
                 'Topic :: Utilities',
                 'License :: OSI Approved :: Apache Software License',
                 
    ],)
