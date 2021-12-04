#!/bin/bash
echo "TODO List as of "`date`
egrep "TODO:" -Hn ../dgtools/*.py|sed -e 's/:[ \t]*#//g'

