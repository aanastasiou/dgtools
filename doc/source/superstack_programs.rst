Programming in Superstack
=========================

This section brings together a number of very small programs that demonstrate some key concepts behind programming 
with just a simple stack.

``Hello World``
---------------

It does not get any more boring than Hello World in Superstack. Simply keep sending values to the output until a zero 
is encountered:

::

    0 100 108 114 111 87 32 111 108 108 101 72 if output fi quit 

A simple calculator is probably a nicer first introduction. Let's ask the user for two numbers add them and show them 
the result:

::

    input input add output quit
    
    
Calculate the sum of a sequence
-------------------------------

::

    0 0 1 8 7 4 5 6 if dup rcycle add cycle pop fi
    
The key idea here is that at the end of the program, the bottom of the stack will contain the sum of all numbers *after
the second zero* (that is, ``1+8+7+4+5+6 = 31``).

:: 

    While the top value is not zero (it is initially 6)
        duplicate the top value
        bring the bottom value to the top of the stack
        add the top two values
        save the top of the stack to the bottom.
        
Did you notice what happened here? We save the sum at the bottom of the stack and on each cycle we add the top two 
numbers. That is whatever number is on the top at the moment plus the sum from the previous operation(s).


Find the length of a sequence
-----------------------------

::

    0 0 1 2 3 4 5 6 7 8 9 10 if rcycle 1 add cycle pop fi

The key idea here is to "save" the current count at the bottom of the stack.

::

    While the top value is not zero (it is initially 10)
        Erase the top value by bringing the bottom value to the top (rcycle)
        push literal 1 to the stack (the top is now ...8,9,0,1)
        Add the top two numbers (that is the current count and 1)
        Send the top of the stack to the bottom
        Pop the top value (which moves to the next value (9)
        

Analytic ``XOR``
----------------

::

    0 0 1 swap cycle swap dup rcycle swap cycle swap dup rcycle 255 xor and cycle pop swap 255 xor and dup rcycle or quit



Find the maximum of a sequence
------------------------------


