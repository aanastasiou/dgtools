============================
Notes on the instruction set
============================

.. note::

    This section applies mainly to the Digirule2/Digirule2A instruction set. The main ideas about providing an 
    efficient instruction set for a CPU that does not have a lot of RAM available still apply to the Digirule 2U 
    as well of course.
    

This section contains a few notes on modifying the instruction set of a Digirule2, so that it becomes more efficient.
Since the Digirule2 has limited memory, it does pay off to implement slightly more complex instructions to save memory 
and this is what is meant here by "efficiency". *Saving bytes of memory while achieving the same end result*.

For example, the Digirule2 instruction set contains both a ``SUBLA`` and an ``ADDLA`` instructions when it could only 
have offered an ``ADDLA`` and let the user perform subtractions in 
`two's complement <https://en.wikipedia.org/wiki/Two%27s_complement>`_ by inverting the second operand.

Here is what this looks like when trying to calculate ``4-2``:

**With** the availability of ``SUBLA``: 

.. code-block:: DigiruleASM

    COPYLA 4
    SUBLA 2
    HALT

*Listing A*

**Without** the availability of ``SUBLA``:

.. code-block:: DigiruleASM

    COPYLA 2
    XORLA 0xFF
    ADDLA 4
    HALT

*Listing B*

Listing A is 5 bytes but listing B is 7 bytes long. In this case, having a separate instruction for addition and 
subtraction helps to fit more instructions into the already limited memory space of the hardware.

This however is not always the case and the following sections offer some suggestions for improvement.

Throughout those: 

* The ``*`` character denotes "any character" when it is not used to denote multiplication. For example, 
  ``SHIFTR*`` is meant to include both ``SHIFTRL, SHIFTRR`` instructions.
  
* ``addr`` denotes an address within the address space of the Digirule2

* ``mem[addr]`` denotes the content of ``addr`` within the address space of Digirule2.


.. _iset_notes_mem_ops:

Memory Operations
=================

Indirect Copy
-------------

As demonstrated in section :ref:`advanced-topics`, there is a clear need for an indirect copy instruction. That is, 
a copy instruction that can copy between memory offsets stored in memory.

Currently, ``COPYRR addr1 addr2`` is a 3 byte instruction that performs ``mem[addr2] = mem[addr1]``. Unless ``COPYRR`` 
is written as a subroutine, it is impossible to get it to copy between two ``addr1, addr2`` that are the result of 
a calculation. However, doing so requires the following pattern:

.. code-block:: DigiruleASM
    :linenos:

    COPY** f_crom
    COPY** f_to
    CALL f_copy

    f_copy:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN

The first two copies denote that ``f_from, f_to`` will definitely have to be populated prior to performing the copy 
and are therefore required, irrespectively of which form they take. They usually are ``COPYRR`` variants though, 
which means that these two copies cost 6 bytes already, plus 3 bytes for the main ``COPYRR`` (denoted here by ``f_copy``),
plus 3 bytes for the costs of ``CALL`` and ``RETURN``, not to mention the cost of calling the function.

That is, 12 bytes of memory to implement an indirect ``COPYRR``. The alternative here would be to have a ``COPYRR`` 
variant that instead of implementing ``mem[addr2] = mem[addr1]``, it implements ``mem[mem[addr1]] = mem[mem[addr2]]``.
In that case, the memory cost would be just 3 bytes.


Arithmetic Instructions
=======================

Target of ``SHIFT**, BCRS*``
----------------------------

Most of the mathematical operations of Digirule 2's instruction set target the Accumulator. For example, addition, 
subtraction (``ADD*A, SUB*A``) and the elementary logic operations or ``AND*A, OR*A, XOR*A`` require one of the 
operands to already be in the accumulator.

The only exception to this are the shifting and bit testing operators.

This means that if a calculation involves an intermediate step where the value of an operand has to be shifted, the 
current value of the accumulator has to be copied to a memory location, shifted there and copied back to the accumulator
to continue with the rest of the calculation.

Both copies would be performed via a ``COPYAR, COPYRA`` which means *a potential loss of 4 bytes of memory*, if the 
calculation cannot be expressed in a different way.

The suggestion here is to have variants of bit testing and shifting that can target the Accumulator too.

``SHIFTRR, SHIFTRL``
--------------------

These two instructions shift bytes left or right and are equivalant to division or multiplication by 2, respectively.
On the Digirule 2, shifting is performed **through** the Carry flag. If a program is performing
a series of operations and it only calls for a plain right or left shift, the Carry flag has to be manually 
cleared so that it does not interfere with the result of the calculation. This inserts 3 bytes for each ``CBR`` 
instruction that ensures that the Carry flag is clear prior to shifting.

One practical example is provided in the Pseudorandom Number Generator (PRNG) that uses a plain Linear Feedback Shift 
Register. In this technique, it is required to shift and XOR the current state of the PRNG to calculate the value of the
bit at its input. 

Therefore, in cases like these, where only a shift is required, offering a plain ``SH*`` instruction would help in
conserving memory.


Flow control instructions
=========================

Indirect ``JUMP`` and ``CALL``
------------------------------

Similarly to the reasoning of the indirect version of ``COPYRR``, an indirect version of ``JUMP addr, CALL addr`` would 
simply jump to memory location ``mem[mem[addr]]``.

To an extent, this is already implemented currently through ``ADDRPC`` but requires an addition and it also does not 
hint at a ``JUMP`` operation.

Being able to transfer execution in such a way would also enable functions to be passed as parameters to other
functions.

Therefore, the suggestion here is to add indirect versions of these two instructions.


