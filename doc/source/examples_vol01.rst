Volume 1 - Complex programs
===========================

The programs in this sections are re-using concepts and 
techniques that are introduced in the ref:`section about the basics <vol_0>`.
        

Implement A Stack
-----------------

What use is a `stack <https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>`_ within a CPU? 
And what if a CPU doesn't have one?

Out of the box, the Digirule2 does not have an internal stack. It is however possible, 
to implement one and this implementation relies heavily on the indirect copy snippet that 
was presented earlier.

.. literalinclude:: ../../dg_asm_examples/stack/stack.dsf
    :language: DigiruleASM
    :linenos:
    

Function calling conventions
----------------------------

The Digirule's instruction set includes a ``CALL`` operation. 
It stores the value of the Program Counter (PC) to the internal stack 
and transfer execution to a different point in memory. Execution 
returns to the calling point once a ``RETURN`` or ``RETLA`` is encountered.

But, calling functions with an arbitrary number of arguments is slightly
different and relies heavily on the CPUs stack. 

This little demo shows a `cdecl(ish) call convention <https://en.wikipedia.org/wiki/X86_calling_conventions>`_ 
to swap two numbers.

.. literalinclude:: ../../dg_asm_examples/stack/funcall.dsf
    :language: DigiruleASM
    :linenos:



Recursion
---------

Being able to call functions, leads naturally to the question *"Can a function call itself?"*.

This is called `recursion <https://en.wikipedia.org/wiki/Recursion_(computer_science)>`_ and is 
a very important concept in computer science (and mathematics), since it allows us to express 
complex iterative processes that are composed of "setup" and repetitive steps.

Having defined a stack on the #Digirule it is relatively easy to express recursion.

This is demonstrated here via the recursive evaluation of a `Fibonacci series <https://en.wikipedia.org/wiki/Fibonacci_number#Sequence_properties>`_
evaluation.

*What is the largest Fibonacci term that the Digirule can compute out of the box?*

*How many steps does it take to do that?*

.. literalinclude:: ../../dg_asm_examples/recfibo/recfibo.dsf
    :language: DigiruleASM
    :linenos:
    

Find the minimum value of an array of integers
----------------------------------------------

One of the more detailed Digirule demos presented here, is that of a
very simple random number generator, using a :ref:`Linear Feedback Shift Register (LFSR) <lfsr>`.
This random number generator, can be used to fill an array with random numbers.

But, what can we do with a set of random numbers?

We can find its minimum (or maximum)

*What modifications would this code snippet require, so that it returns the maximum value of the array?*  


.. literalinclude:: ../../dg_asm_examples/findmin/findmin.dsf
    :language: DigiruleASM
    :linenos:
    

Sorting an array of integers
----------------------------

Bubble Sort, Shaker Sort, Quicksort, Merge Sort, Heap sort, Insertion sort....Delay sort!

So many different ways to enforce order to a list of items.

This is a demonstration of the simplest, most primitive and slowest algorithm that is based on 
finding the minimum (or maximum) element in an array: "Selection Sort".

The algorithm is composed of two steps: 

1. Find the minimum of an array of :math:`N-n` numbers starting at position :math:`n`, 
2. Move that minimum value to position :math:`n`
3. Repeat from step 1 while :math:`n<N`

*As is, the agorithm sorts a list of integers in ascending order. What modifications would make the algorithm to sort in descending order?*


.. literalinclude:: ../../dg_asm_examples/simplesort/selectsort.dsf
    :language: DigiruleASM
    :linenos:
    


Longest Ripple Counter Ever
---------------------------

A ripple counter is the basic building block of timers.

To understand its operation, consider what happens to some ``i`` 
when we increase its value via a ``i=i+1`` (or ``i++`` for short) : ::

      MSb    LSb  Decimal
    ----------------------
     0b00000000     0
     0b00000001     1
     0b00000010     2
     0b00000011     3
     0b00000100     4
     0b00000101     5
     0b00000110     6
     0b00000111     7
     ..........    ...
     0b11111111    255
    
Notice the Least Significant bit (LSb), it continuously "pulses" between 
``0`` and ``1``. Once the LSb counts 1, it resets and "pulses" its 
neighbour *to the left* (towards the Most Significant bit (MSb)).

This continues until ``i`` now assumes the value 255 (or ``0b11111111`` in 
binary).

Now, something special happens: If we try to ``i++`` once more, ``i`` **wraps around** 
and hits zero again.

At that point, we have counted 255. At that point, if we had a 9bit wide 
variable for ``i``, we could "bump" that to ``1`` and that would denote 
*"1 twohundredfiftyfiven" PLUS whatever i contains*.

In fact, we can extend that idea to create arbitrary length ripple counters:

* Increase variable ``a``
    * Once ``a`` **wraps around** increase ``b``
        * Once ``b`` **wraps around** increase ``c``
            * Once ``c`` **wraps around** increase ``d``
                * Once ``d`` **wraps around** increase ``e``
    
And so on until we run out of memory.

Notice here the distinction between **b** its and **B** ytes.

In the following Digirule2 program, we use the exact same concept to 
construct a ripple counter that is 233 bytes long.

Consequently it can count from 0 to :math:`2^{233}`.

That number is: ::
    
    1317989400684132247985462012217008492691201352246603794343706666106002621345561402409288057184803891421955702295376321167301153177543164830484060369180090017640453495090693794266442291580023684417164027872494288824399014228601614308240494248737033497020218523643351874839672280540716174154647379870729350964002203580783694150516875895770731889313358644413955737374858503352890882385294315489946453488394423398674401553548965414666791756989103381598433903560751938491589040648835760728486421431223385020250955241295200644184289426016410194726827646163765077999616

(Seriously, just type ``2**233`` on a Python interpreter)


So What?
^^^^^^^^

There is no single battery that will keep this counter going until it counts to its maximum.
There is no single lifetime within which to see it wrapping around.

Suppose that it takes the Digirule aproximately :math:`60e-6` seconds to increase the counter 
by 1. That is 60 microseconds.

* This means that this number, describes :math:`7.90793640410479348791e556` seconds.
    * Divided by 3600 seconds in an hour, it describes :math:`2.19664900114022041331e553` hours.
        * Divided by 24 hours in a day, it describes :math:`9.15270417141758505545e551` days.
            * Divided by 30 days in a month, it describes :math:`3.05090139047252835182e550` months.
                * Divided by 12 months in a year, it describes :math:`2.54241782539377362651e549` years.
                    * Divided by 100 years in a century, it describes :math:`2.54241782539377362651e547` centuries.
                        * Divided by 1000 years in a millenium, it descrbes :math:`2.54241782539377362651e544` millenia.

That is :math:`\approx 2.54 \times 10^{544}` **millenia**.


.. literalinclude:: ../../dg_asm_examples/longcounter/longcounter.dsf
    :language: DigiruleASM
    :linenos:
