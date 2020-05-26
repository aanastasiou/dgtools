Quick Programs
==============

Tweetable ``dgasm`` code demonstrations.


``Hello World``
---------------

Perhaps the simplest program in DigiruleASM

.. literalinclude:: ../../data/quickprogs/hellosum/hellosum.dsf
    :language: DigiruleASM
    :linenos:
    
Assignment
----------

Assigning a literal
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/assignments/assign1.dsf
    :language: DigiruleASM
    :linenos:
    

Assigning to expression
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/assignments/assign2.dsf
    :language: DigiruleASM
    :linenos:
    
.. literalinclude:: ../../data/quickprogs/assignments/assign3.dsf
    :language: DigiruleASM
    :linenos:


Assignment with indirect addressing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: DigiruleASM
    :linenos:
    
    # Indirect addressing in Digirule2
    #
    # Notice here: COPYLR loads a literal to 
    # some memory location. In this case, 
    # the literal is simply the **address** of the label.
    #
    # This snippet implements R2=R0
    #
    # Set the values of the source (R0) and destination (R1)
    COPYLR R0 f_from 
    COPYLR R2 f_to
    # Execute the copy
    CALL f_copy_ind
    HALT
    
    # R0 is a label. A label resolves to the address it
    # is pointing.
    #
    # .DB is a dgasm directive that initialises memory to 
    # some literal numeric value (e.g. 0,1,2 and so on)
    R0:
    .DB 0
    R1:
    .DB 1
    R2:
    .DB 2
    
    
    # Indirect copy via self-modification.
    # We construct a suitable absolute 
    # addressing copy instruction (COPYRR) and 
    # execute it as a sub-routine
    f_copy_ind:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN



Swapping the values of two variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/simpleswap/swap_simple.dsf
    :language: DigiruleASM
    :linenos:
    
    
.. literalinclude:: ../../data/quickprogs/simpleswap/swap_indirect.dsf
    :language: DigiruleASM
    :linenos:


Numeric Comparisons
-------------------

Have you ever wondered what comparison operators resolve to? Comparisons are 
resolved to humble subtractions if a-b==0 the numbers are equal, a-b<0 means 
that a<b. <= and >= are cascaded logical ORs of the individual operations.

.. literalinclude:: ../../data/quickprogs/compop/compop_lt.dsf
    :language: DigiruleASM
    :linenos:
    
.. literalinclude:: ../../data/quickprogs/compop/compop_leq.dsf
    :language: DigiruleASM
    :linenos:



For loops
---------

Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. literalinclude:: ../../data/quickprogs/forloop/forloop.dsf
    :language: DigiruleASM
    :linenos:


Array Indexing
--------------


.. literalinclude:: ../../data/quickprogs/arrayindexing/arrayindexing.dsf
    :language: DigiruleASM
    :linenos:
    

Copy a memory block
-------------------

.. literalinclude:: ../../data/quickprogs/copymemblock/copymemblock.dsf
    :language: DigiruleASM
    :linenos:
    

Swap values between two memory blocks
-------------------------------------

.. literalinclude:: ../../data/quickprogs/swapmemblock/swapmemblock.dsf
    :language: DigiruleASM
    :linenos:



Find minimum num in an array
----------------------------

Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. literalinclude:: ../../data/quickprogs/findmin/findmin.dsf
    :language: DigiruleASM
    :linenos:
    

Sort an array
-------------

.. literalinclude:: ../../data/quickprogs/simplesort/selectsort.dsf
    :language: DigiruleASM
    :linenos:


The Quick Brown Fox Jumps Over The Lazy Dog
-------------------------------------------

.. literalinclude:: ../../data/quickprogs/qbfjold/qbfjold.dsf
    :language: DigiruleASM
    :linenos:
