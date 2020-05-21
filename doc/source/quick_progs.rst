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

.. code-block:: DigiruleASM
    :linenos:
    
    COPYLR 1 R0
    HALT
    
    R0:
    .DB 0
    
Assigning between variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: DigiruleASM
    :linenos:
    
    COPYRR R1 R0
    HALT
    
    R0:
    .DB 1
    R1:
    .DB 42
    

Swap the values of two variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: DigiruleASM
    :linenos:
    
    COPYRR R0 R2
    COPYRR R1 R0
    COPYRR R2 R1
    HALT
    
    R0:
    .DB 1
    R1:
    .DB 42
    R2:
    .DB 0
    

Indirect copy
^^^^^^^^^^^^^

.. code-block:: DigiruleASM
    :linenos:
    
    # Swap with indirect copy 
    COPYLR R0 f_from 
    COPYLR R2 f_to
    CALL f_copy_ind
    COPYLR R1 f_from 
    COPYLR R0 f_to
    CALL f_copy_ind
    COPYLR R2 f_from 
    COPYLR R1 f_to
    CALL f_copy_ind
    HALT
    
    R0:
    .DB 0
    R1:
    .DB 1
    R2:
    .DB 2
    
    f_copy_ind:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN
    


Numeric Comparisons
-------------------

Have you ever wondered what comparison operators resolve to? Comparisons are 
resolved to humble subtractions if a-b==0 the numbers are equal, a-b<0 means 
that a<b. <= and >= are cascaded logical ORs of the individual operations.

.. literalinclude:: ../../data/quickprogs/compop/compop.dsf
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
