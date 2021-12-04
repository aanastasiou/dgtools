#!/usr/bin/env python
"""

Usage: dgform.py [OPTIONS] INPUT_FILE

  Generates an HTML file with code formatted through the DigiruleASM
  pygments formatter.

Options:
  --help  Show this message and exit.

\f
:author: Athanasios Anastasiou
:date: May 2020
"""
from pygments import highlight
from pygments.formatters import HtmlFormatter
import sys
import click 
from dgtools import DigiruleASMLexer


@click.command()
@click.argument("input_file", type=click.File("rb"))
def dgform(input_file):
    """
    Generates an HTML file with code formatted through the DigiruleASM pygments formatter.
    Output is sent to stdout.
    """
    sys.stdout.write(highlight(input_file.read(), 
                               DigiruleASMLexer(), 
                               HtmlFormatter(full=True,
                                             cssfile="dgform_theme.css",
                                             linenos="table")))
    

if __name__ == "__main__":
    dgform()
