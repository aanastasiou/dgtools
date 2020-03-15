#!/bin/bash
echo "TODO List as of "`date`
egrep "TODO:" -Hn ../src/dgasm.py ../src/dginspect.py ../src/dgsim.py|sed -e 's/:[ \t]*#//g'

