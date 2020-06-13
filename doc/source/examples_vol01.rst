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

A ripple counter and a relatively accurate clock signal source are the basic building blocks of digital timers.

All that a ripple counter does is count clock pulses. Now, suppose we have some ``i`` 
and we start counting in binary by repeatedly calling ``i=i+1`` (or ``i++`` for short).

The values of ``i`` will be:

::

    MSb    LSb  Decimal
 bit 76543210
    -------------------
     00000000     0
     00000001     1
     00000010     2
     00000011     3
     00000100     4
     00000101     5
     00000110     6
     00000111     7
     ........    ...
     11111111    255
    
Bit 0, the Least Significant bit (LSb), counts :math:`0,1` and then resets and 
"signals" bit 1, its neighbour *to the left* to count :math:`1`. Once bit 1 has 
counted its maximum (:math:`0,1`) it will reset and "signal" bit 2, its neighbour
*to the left* to count :math:`1`....And so on, all the way to the Most 
Significant bit (MSb)).

From this point of view a ripple counter is just a chain of tiny little elementary 
counters, each one counting to its maximum and then advancing the next counter.


This continues until ``i`` now assumes the value 255 (or ``11111111`` in 
binary). Now, something special happens: If we try to ``i++`` once more, ``i`` 
**wraps around** and hits zero again.

This is a fancy way of saying ``i`` resets and we could "catch" that event 
and use it to increase another variable (``j``) to start counting. This, would 
now look like: 

* Increase variable ``i``
    * Once ``i`` **wraps around** increase ``j``
        * Once ``j`` **wraps around** increase ``k``
            * Once ``k`` **wraps around** increase ``l``
                * Once ``l`` **wraps around** increase ``m``
    
And so on until we run out of memory.

In the following Digirule2 program, we use this concept to 
construct a ripple counter that is 224 **BYTES** long.

(Notice here the distinction between bit and Byte.)

A 1 byte long counter can count from :math:`0` to :math:`2^{1 \times 8} - 1`, or :math:`255`.

A 224 byte long counter can count from :math:`0` to :math:`2^{224 \times 8} - 1` or ... ::
    
    279095111627852376407822673918065072905887935345660252615989519488029661278604994789701101367875859521849524793382568057369148405837577299984720398976429790087982805274893437406788716103454867635208144157749912668657006085226160261808841484862703257771979713923863820038729637520989894984676774385364934677289947762340313157123529922421738738162392233756507666339799675257002539356619747080176786496732679854783185583233878234270370065954615221443190595445898747930123678952192875629172092437548194134594886873249778512829119416327938768895

This number is big.


How Long Is Long?
^^^^^^^^^^^^^^^^^

Suppose that it takes the Digirule aproximately :math:`60e-6` seconds [1]_ to increase the counter 
by 1. That is 60 microseconds.

* This means that this number, describes :math:`1.67457066976711425845e535` seconds.
    * Divided by 3600 seconds in an hour, it describes :math:`4.6515851937975396068e531` hours.
        * Divided by 24 hours in a day, it describes :math:`1.93816049741564150283e530` days.
            * Divided by 30 days in a month, it describes :math:`6.46053499138547167611e528` months.
                * Divided by 12 months in a year, it describes :math:`5.38377915948789306342e527` years.
                    * Divided by 100 years in a century, it describes :math:`5.38377915948789306342e525` centuries.
                        * Divided by 100 centuries in a millenium, it describes :math:`5.38377915948789306342e523` millenia.

That is :math:`\approx 5.4 \times 10^{523}` **millenia**.

There is no single battery that will keep this counter going until it counts to its maximum.

There is no single lifetime (devoted to maintaining a running Digirule) within which to see its value wrap around.


And while this counter scans through each and every value between :math:`0` and :math:`2^{1792}` as it gallops through 
the millenia, it also goes through **ALL** the possible Digirule 2 programs that can be constructed in 224 bytes and, 
all the possible phrases in English [2]_ that can be described in 224 bytes.


.. literalinclude:: ../../dg_asm_examples/longcounter/longcounter.dsf
    :language: DigiruleASM
    :linenos:
    
.. [1] Brent Hauser responded with all the details about the Digirule2's timings on the Discord server. The 60 micro 
       second estimate is a conservative estimate of the Digirule's timing to execute the counter program. If the 
       hardware counts a bit slower than that, then the millenia will keep piling up. Even if the Digirule was made 
       to run 1 order of mangitude faster, that would only knock off one order of magnitude from that :math:`...e51`.
       It would still be, a big number.

.. [2] "...phrases in English" is the quicker thing to describe here, since the ASCII table contains direct
       correspondences of numbers to English characters. If the memory was interpreted as Unicode, all languages would 
       be possible but in that case, the maximum number of letters described by 224 bytes would varry.
