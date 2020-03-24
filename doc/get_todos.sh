#!/bin/bash
echo "TODO List as of "`date`
egrep "TODO:" -Hn ../src/*.py|sed -e 's/:[ \t]*#//g'

