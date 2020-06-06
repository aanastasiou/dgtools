.. _vol_0:

Volume 0 - Basics
=================


``Hello World``
---------------

This is the shortest Digirule ASM program. 

You can key it in by entering the numbers ``4,1,8,1,0``, or you can ``dgasm`` and ``dgsim`` it first. 

.. literalinclude:: ../../dg_asm_examples/hellosum/hellosum.dsf
    :language: DigiruleASM
    :linenos:
    
    
The Quick Brown Fox Jumps Over The Lazy Dog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is a `pangram phrase <https://en.wikipedia.org/wiki/Pangram>`_ where every letter of English is 
used exactly once. 

The following code snippet is the Digirule ASM equivalent where every operation is used exactly once. 

.. literalinclude:: ../../dg_asm_examples/qbfjold/qbfjold.dsf
    :language: DigiruleASM
    :linenos:


Assignments
-----------

Most programming languages have assignments. But, just typing ``a=42`` in an editor, is not enough. 

Something must realise the intention. Here is what assignments come down to on the Digirule.


Assigning a literal
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/assignments/assign1.dsf
    :language: DigiruleASM
    :linenos:
    

Assigning to expression
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/assignments/assign2.dsf
    :language: DigiruleASM
    :linenos:
    

Assigning to expression with indirect addressing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/assignments/assign3.dsf
    :language: DigiruleASM
    :linenos:



Swapping the values of two variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can just "swap two variables", or you can use `Parallel Assignment <https://en.wikipedia.org/wiki/Assignment_(computer_science)>`_ 


On the Digirule, it is a matter of 3 or 15 clock ticks. 

*Remember which algorithm uses so many swaps that it gets all...fizzy?*

Swap two variables
^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/simpleswap/swap_simple.dsf
    :language: DigiruleASM
    :linenos:
    

Swap with indirect copy
^^^^^^^^^^^^^^^^^^^^^^^
    
.. literalinclude:: ../../dg_asm_examples/simpleswap/swap_indirect.dsf
    :language: DigiruleASM
    :linenos:
    

Array Indexing
--------------

Up here, we can write ``my_array[5]`` but this implies not one but two operations: 

#. Discover the address
#. Fetch from address. 

Here is how arrays are expressed on the Digirule. 

.. literalinclude:: ../../dg_asm_examples/arrayindexing/arrayindexing.dsf
    :language: DigiruleASM
    :linenos:


Conditional branching & the ``if`` command
------------------------------------------

When you write ``if (R0 < R1) {} else {};``, how is this evaluated by a CPU? 

What does an ``IF`` look like when it comes to actually **doing it**.

Here it is, on a Digirule, the simplest form of `flow control <https://en.wikipedia.org/wiki/Control_flow>`_. 

.. literalinclude:: ../../dg_asm_examples/compop/compop_lt.dsf
    :language: DigiruleASM
    :linenos:
    

There is a difference between ``if (R0 < R1)...;`` and ``if (R0<=R1)...;`` and on the Digirule
that difference is 2 clock cycles. 

*EVERY symbol counts.*

.. literalinclude:: ../../dg_asm_examples/compop/compop_leq.dsf
    :language: DigiruleASM
    :linenos:
    

Iteration
---------

We already saw some simple flow control in Digirule ASM. 

Diverting execution depending on an expression soon leads to doing things repeatedly until a condition is met.

Here we re-use that to show``FOR`` and ``WHILE`` ASM code equivalents on a Digirule.


.. literalinclude:: ../../dg_asm_examples/forloop/forloop.dsf
    :language: DigiruleASM
    :linenos:

    

Copying a memory block
^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/copymemblock/copymemblock.dsf
    :language: DigiruleASM
    :linenos:
    

Swapping values between two memory blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../dg_asm_examples/swapmemblock/swapmemblock.dsf
    :language: DigiruleASM
    :linenos:
