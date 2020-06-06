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



.. Find minimum num in an array
.. ----------------------------

.. Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. .. literalinclude:: ../../dg_asm_examples/findmin/findmin.dsf
..     :language: DigiruleASM
..     :linenos:
    

.. Sort an array
.. -------------

.. .. literalinclude:: ../../dg_asm_examples/simplesort/selectsort.dsf
..     :language: DigiruleASM
..     :linenos:
