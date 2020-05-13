Quick Programs
==============

Tweetable ``dgasm`` code demonstrations.


``Hello World``
---------------

.. literalinclude:: ../../data/quickprogs/hellosum/hellosum.dsf
    :language: DigiruleASM
    :linenos:
    

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

Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. literalinclude:: ../../data/quickprogs/arrayindexing/arrayindexing.dsf
    :language: DigiruleASM
    :linenos:


Find minimum num in an array
----------------------------

Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. literalinclude:: ../../data/quickprogs/findmin/findmin.dsf
    :language: DigiruleASM
    :linenos:
