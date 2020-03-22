.. _advanced-topics:

Advanced Digirule 2 Programming
===============================

``dgtools`` provides an assembler that can manage labels as memory addresses and this makes it possible to start 
creating more involved programs. 

However, one thing that the Digirule hardware itself does not specify is a stack which is an important part of 
more complex programs that include function calling.

This section first establishes a stack and associated operations (push, pop), later a set of registers and finally 
based on these pre-requisites it demonstrates function calling with parameters passed on the stack.


Defining a Stack
----------------

The Digirule 2 is capable of referencing approximately 256 bytes of main memory. Therefore, it should be possible to 
implement a stack as a statically allocated array of ``N`` values where the push and pop operations are carried out 
at the "head" of the stack.

The only problem here is that the Digirule 2 instruction set does not support **indirect memory access**. The command 
`COPYRR` copies memory **content** from one address to another address but (out of the box) it cannot copy memory from 
the **value** of a memory address (i.e. where a memory location is pointing to), to the **value** of another address. 

Implementing indirect memory access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To achieve this, we are going to use the label capabilities of ``dgasm`` to "build" a ``COPYRR`` that can copy memory 
indirectly. 

This is achieved by writing a "template" function:

.. code::

    f_copy_by_ref:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN


This is part of :download:`../../data/advanced/stack.asm`

The first byte (``7``) is the opcode of ``COPYRR``, the second byte is labeled ``f_from`` and the third byte is 
labeld ``f_to``.

The CPU is "tricked" into thinking that it executes a ``COPYRR`` but this is now a parametrisable ``COPYRR`` that copies
between two addresses that can be the result of any computation performed by the code.

To copy between two references, **calculate** the references (if required), move the references to addresses ``f_from`` 
and ``f_to`` and then execute a ``CALL f_copy_byref``. The CPU will fetch the ``7``, decide it is a ``COPYRR``, read in 
the next two bytes, perform the copy, hit the RETURN and go back to where it was called from.


Getting the "head" of the stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Defining the stack through ``dgasm`` is as trivial as defining a label and immediately populating it with values. For 
example:

.. code::

    stack:
    .DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F


There is no particular reason for these default values other than making this memory range stand out in a memory dump.

The stack also needs a way of pointing to its head address.

.. note::

    A [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) is a data structure that can store and retrieve
    data through the operations of push and pop respectively. Both storage and retrieval are performed from a **single**
    end-point that always points at the top of the stack. Most commonly, this is called the "head" of the stack.
    

This can be achieved by using another "labeled" location:

.. code::

    stack_ptr:
    .DB 0

Having defined the stack, we now need to define its two fundamental operations: ``push, pop``. This is relatively easy, 
all we have to do is find out where the head is pointing to and send (or retrieve) a number to (or from) that location.
This is achieved with:

.. code::

    f_push:
    CALL f_get_stack_head
    COPYAR f_to
    COPYLR r0 f_from
    CALL f_copy_by_ref
    INCR stack_ptr
    RETURN

    f_pop:
    DECR stack_ptr
    CALL f_get_stack_head
    COPYAR f_from
    COPYLR r0 f_to
    CALL f_copy_by_ref
    RETURN

    f_get_stack_head:
    COPYLA stack
    ADDRA stack_ptr
    RETURN


This is part of :download:`../../data/advanced/stack.asm`


.. note::

    This is a bit of an overkill for getting the head of a stack, because it assumes that the head has to 
    be re-calculated prior to every push or pop. Such a mode of access would be necessary in the case of an array 
    where elements can be stored to or read from *randomly* across any element of the array. Since the head of the 
    stack can only be increased or decreased and is being assigned to its own memory space, a much faster way of 
    working with it here would be to establish ``f_get_stack_head`` as ``f_init_stack`` and then use ``stack_ptr`` 
    directly at subsequent calls.

But for these examples, we will take the scenic route, as it makes the program traces more interesting too.

All that ``f_push, f_pop`` do is to calculate where the head of the stack is and then pass that address as either the 
``f_from`` or ``f_to`` "parameter" of a made-up ``COPYRR`` that now copies by reference.

**But**, how are these "low level" functions going to communicate with the rest of the code? The Digirule 2 does not 
specify a standardised register set.

By now, it should be clear that this is not a problem at all because we can use the labeled `.DB` capabilities of the 
assembler, to specify the equivalent of a "register" or even a complete set of registers.

For the purposes of this example, register ``r0`` is used as the intermediate register for the ``f_push, f_pop`` 
functions.

The complete example below pushes values `0,1,2,3,2,1,0,1,2` to the stack and terminates:

.. code::

    start:
    COPYLR 0 r0
    CALL f_push
    COPYLR 1 r0
    CALL f_push
    COPYLR 2 r0
    CALL f_push
    COPYLR 3 r0
    CALL f_push
    COPYLR 2 r0
    CALL f_push
    COPYLR 1 r0
    CALL f_push
    COPYLR 0 r0
    CALL f_push
    COPYLR 1 r0
    CALL f_push
    COPYLR 2 r0
    CALL f_push
    HALT

    f_push:
    CALL f_get_stack_head
    COPYAR f_to
    COPYLR r0 f_from
    CALL f_copy_by_ref
    INCR stack_ptr
    RETURN

    f_pop:
    DECR stack_ptr
    CALL f_get_stack_head
    COPYAR f_from
    COPYLR r0 f_to
    CALL f_copy_by_ref
    RETURN

    f_get_stack_head:
    COPYLA stack
    ADDRA stack_ptr
    RETURN

    f_copy_by_ref:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN


    r0:
    .DB 0

    stack_ptr:
    .DB 0
    stack:
    .DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F


This listing is available in :download:`../../data/advanced/stack.asm`


Function calls using a stack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that the Digirule 2 has a stack, it can call any function with any number of argument by 
adopting a `"calling convention" <https://en.wikipedia.org/wiki/Calling_convention>`_ and defining a standardised 
set of registers.

In this section, the addition of two numbers is performed within the following two argument function:

.. code::

    q_add_ab:
    CALL f_pop
    COPYRR r0 t0
    CALL f_pop
    COPYRR r0 t1
    COPYRA t0
    ADDRA t1
    COPYAR r0
    CALL f_push
    RETURN


This is part of :download:`../../data/advanced/funcall.asm`

Here, ``q_add_ab`` first pops the numbers from the stack to "temporary registers", performs the addition, pushes the 
result back on to the stack and returns. All that the caller has to do now is to pop the stack on the "other side of 
the call" to retrieve the result.

The complete listing is now:

.. code::

    .EQU a=1
    .EQU b=2

    start:
    COPYLR a r0
    CALL f_push
    COPYLR b r0
    CALL f_push
    CALL q_add_ab
    CALL f_pop
    COPYRR r0 255
    HALT

    q_add_ab:
    CALL f_pop
    COPYRR r0 t0
    CALL f_pop
    COPYRR r0 t1
    COPYRA t0
    ADDRA t1
    COPYAR r0
    CALL f_push
    RETURN

    f_push:
    CALL f_get_stack_head
    COPYAR f_to
    COPYLR r0 f_from
    CALL f_copy_by_ref
    INCR stack_ptr
    RETURN

    f_pop:
    DECR stack_ptr
    CALL f_get_stack_head
    COPYAR f_from
    COPYLR r0 f_to
    CALL f_copy_by_ref
    RETURN

    f_get_stack_head:
    COPYLA stack
    ADDRA stack_ptr
    RETURN

    f_copy_by_ref:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN


    r0:
    .DB 0
    r1:
    .DB 0
    r2:
    .DB 0
    r3:
    .DB 0
    r4:
    .DB 0
    r5:
    .DB 0
    r6:
    .DB 0
    r7:
    .DB 0

    t0:
    .DB 0
    t1:
    .DB 0
    t2:
    .DB 0
    t3:
    .DB 0
    t4:
    .DB 0
    t5:
    .DB 0
    t6:
    .DB 0
    t7:
    .DB 0

    stack_ptr:
    .DB 0
    stack:
    .DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F


This is listing :download:`../../data/advanced/stack.asm`.

It is basically a continuation of listing :download:`../../data/intro/simpleadd_5.asm` and it could be called 
externally as per :ref:`this example from the introductory section <cplx_intro_example_5>`.


Conclusion
----------

Now that Digirule 2 has a stack and a set of standardised registers, it is possible to start thinking about implementing 
a higher level language that compiles down to its assembly.

It should then be possible to write arbitrarily complex programs to carry out functionality possibly not envisaged for
the Digirule 2.

But, aside from being 8bit and having a very limited amount of memory, there is nothing that can be expressed with a 
`"stack machine" <https://en.wikipedia.org/wiki/Stack_machine>`_ that Digirule cannot do.

It might be slow and somewhat difficult to define, but Digirule will eventally compute it.

