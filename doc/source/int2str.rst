.. _itoa:

Converting numbers to strings
=============================

As a segway to more complex mathematical functions, let's tackle converting an integer from its usual numeric 
representation (e.g. 243) to its string representation (e.g. "243").

You might be thinking: *"What is the point? I just call a PRINT statement and it prints the number"*, but what is it
that the PRINT command really does? And why is that linked to mathematical operations such as multiplication 
and division...and why are these *"more complex"* ???.

The short answer is that computers do not really know how to PRINT stuff in the same way that they know how to add or
subtract numbers.

For example, out of the box the Digirule2 does not handle numbers "wider" than 8 bits. Even if we implement 16 bit 
integers along with their 4 fundamental operations (mul, div, add, sub), we would still not be able to "see" those 2 
individual bytes as 1 number. That is, the number 939 (``0b 0000 0011 | 1010 1011``) would only be "perceived" as 
``0x03, 0xAB``. The point of the conversion here is to go from ``0x03, 0xAB`` to ``"939"``. 
 
Coincidentally, the key mathematical operation behind converting an integer from its binary 
representation to a **human readable** (decimal) representation, is *division*, which, the Digirule2 does not have an 
operation for.

Let's give Digirule the capability to print the string representation of numbers...


Outline of the conversion
-------------------------

The key tool in converting numbers to `glyphs <https://en.wikipedia.org/wiki/Glyph>`_ that spell out a value, is the 
`ASCII table <https://en.wikipedia.org/wiki/ASCII>`_. 

This is a standard feature of modern computers and it is a part of memory that contains **pictures** that correspond 
to **numbers**. When you try to print a string via a language's ``print`` functions, the computer scans the string, 
looks up the **pictures** that correspond to the bytes composing the string and sends them off to video memory.

From the point of view of the computer, the word ``Digirule`` looks like ``[68, 105, 103, 105, 114, 117, 108, 101]``, 
with ``68`` being the *code* for the *picture* of ``D``, in the `ASCII table <https://ascii.cl/>`.

And similarly, from the point of view of the computer, the word ``137``, looks like ``[49, 51, 55]``, with ``49`` being 
the code for ``1``.

Therefore, to **print** a number in a human readable (decimal) form, all we have to do is break it down to its composing 
powers of 10 and then "adjust" those coefficients for their ASCII representation.

For example, ``137`` is:


.. math::

    137 = 1 * 10^2 + 3 * 10^2 + 7 * 10^0
    
Similarly, ``17329`` is:

.. math::

    17329 = 1 * 10^4 + 7 * 10^3 + 3 * 10^2 + 2*10^1 + 9 * 10^0

The difference between ``1`` as a number and ``"1"`` (a string) is that ``"1"`` is actually the number 49.

Therefore, at its heart, the conversion of a single number in the range ``0-9``, to its human readable (decimal) form 
comes down to *adding 48* (the value for ``"0"``) to that number.

With this in mind and the way numbers are composed by their constituent powers of 10, we can start piecing together 
a generic conversion algorithm:

* Given the bit depth (:math:`b`) of a number, work out the highest power of 10 (:math:`d`) possible.
    * For example, for :math:`b=8` bit integers, the largest number is ``255`` which means that the highest power of 
      10 here would be :math`d=2` (because :math:`255 = 2 * 10^2 + 5 * 10^1 + 5 * 10^0`.)
      
* Now, to get the coefficient of the "hundreds", perform an integer division by :math:`10^2 = 100`
    * :math:`255 \backslash 100 = 2`
        * Ratio     : :math:`2`
        * Remainder : :math:`55`
    * Convert the Ratio to a character by adding ``48``: :math:`2+48=50`
    * **Output:** ``50``
    
* Take the remainder and perform integer division by :math:`10^1 = 10`
    * :math:`55 \backslash 10 = 5``
        * Ratio     : :math:`5`
        * Remainder : :math:`5`
    * Convert the Ratio to a character by adding ``48``: :math:`5 + 48 = 53`
    * **Output:** ``53``
    
* Take the remainder and perform integer division by :math:`10^0 = 1`
    * There is no reason to divide by 1 here, therefore, let's simply say:
        * Ratio     : :math:`5`
        * Remainder : :math:`0`
    * Convert the Ratio to a character by adding ``48``: :math:`5 + 48 = 53`
    * **Output:** ``53``
    
And this is how the number ``255`` is converted to the character sequence (a.k.a string) ``[50, 53, 53]``

Fantastic! That's so repeatable and well defined, let's get coding!!

Slight problem here: The Digirule2 ASM does not include a command to perform the integer division step. Out of the box, 
we have absolutely no way of realising all these divisions by the powers of 10.

Out of the box, it is impossible to divide.


Dividing Integers
-----------------

The Digirule2 ASM only contains low level commands for addition (``ADDLA, ADDRA``) and subtraction (``SUBLA, SUBRA``).
In other words, at its lowest level, the chip does not "know" how to divide two numbers.

But that is not too much of a problem. If you think about it, multiplication of some number :math:`a` by 
another number :math:`b` is "shorthand" for "add :math:`a`, :math:`b` times". Similarly, it is not difficult to think 
about the **reverse operation** of division of some integer :math:`a` by another integer :math:`b` as "shorthand" for 
"keep subtracting :math:`b` from :math:`a` and tell me how many times it fits and what, if anything, remains".

Now, it is worth noting here that multiplication and division have long [#1]_ been seen as **iterative processes** and 
wherever there is **iteration**, there is a strong motivation for simplifying it and even making it faster where 
possible.

The wikipedia pages on `division <https://en.wikipedia.org/wiki/Division_algorithm>`_ and 
`multiplication <https://en.wikipedia.org/wiki/Multiplication_algorithm>`_ algorithms are a very good start for more 
information about those algorithms.

Different algorithms suit different needs.

For the purposes of this routine of converting integers to strings, here, we will use the very simple iterative version
of division where we simply keep subtracting the *divisor* from the *dividend* until it cannot be divided any more.

This is as follows:

Given two numbers :math:`a` (The *dividend*, the number to divide) and :math:`b` (The *divisor*, the number to divide
by) and aiming to produce two numbers :math:`R` (The *ratio* :math:`a \backslash b`) and :math:`M` (The *remainder*) :

1. Set :math:`R=0`, :math:`M=a`
2. Perform :math:`R = R + 1`
3. Perform :math:`M = M - b`
4. Check if the subtraction produced a negative number
    * If it did not, continue from step 5
    * If it did continue from 6
5. Check if the subtraction produced ``0`` (zero)
    * If it did not, continue from step 2
    * If it did continue from step 8
6. Perform :math:`M = M + b` (Need to adjust :math:`M` because it already produced the negative number)
7. Perform :math:`R = R - 1` (Need to adjust :math:`R` because it would have overshot the ratio)
8. **STOP**


Now, all calculations within steps 1-8 can be performed with Digirule2 ASM and in addition, the Digirule2 can now 
perform integer division for 8bit numbers, which means that there is nothing stopping us from implementing the 
``int2str`` function above.



.. [#1] And by "long" here we mean **thousands** of years.



Putting it all together
-----------------------

So, now we are ready to start writing some ASM. And this, again, includes some "housekeeping" details that require some
planning on their own right.

This is because when we were outlining the algorithms above, we may have given names to variables or never bothered 
with the limitation of not having an infinite ammount of memory which we can use to store our values in. Or any other 
constraints that may be imposed on us by the hardware (You cannot have floating point (:math:`\mathbb{R}`) numbers, you 
cannot add without using the Accumulator and so on).

We would be aiming to write a stand-alone routine that is generic and re-usable in other programs too and one that 
interferes with the state of the processor as little as possible.

For this purpose, in the following listing, I am using some generic registers ``r0, r1, r2, ...`` and so on and some 
"temporary registers". The purpose of the generic registers here is to pass parameters and hold the result of
computations and the purpose of the temporaries is to hold intermediate stage of computation results.

For more details, please see inline code comments below:

.. code-block:: DigiruleASM
    :linenos:
    :name: int2str

    .EQU status_reg=252

    # Program Entry Point
    # Convert decimal 255 to string in variable `asc_string`
    COPYLR 255 r0
    COPYLR ascii_str r1 # This COPYLR copies the VALUE of the label to r1. The value of the label is its MEMORY ADDRESS.
    CALL int2str
    HALT

    int2str:
    # Transforms an integer to an ASCII representation
    # Input:
    #    r0: int
    #    r1: Address of the first byte of the string
    # Note:
    #    The Digirule2 does not understand the string data type. In this 
    #    example, a "string" is just three sequential bytes in memory, 
    #    starting at the memory address indicated by register r1.
    #
    # Save the arguments because they will be required later
    COPYRR r0 t0
    COPYRR r1 t1
    # Divide by 100
    COPYRA r0
    COPYLR 100 r0
    CALL div
    # Adjust the ascii rep and copy to the next available string position
    CALL int2str_adjust_and_copy
    # Load the remainder, divide by 10 
    COPYRA r0
    COPYLR 10 r0
    CALL div
    CALL int2str_adjust_and_copy
    # Load the remainder
    # Notice here, the remainder is in r0 but it does not 
    # go through the division. For this reason, it is simply
    # copied across from r0 to r1 to be able to re_use the 
    # adjust_and_copy procedure as is.
    COPYRR r0 r1
    CALL int2str_adjust_and_copy
    RETURN
    int2str_adjust_and_copy:
    # Adds the ascii 0 value (48) to the order of mag multiplier 
    # and puts the result to the next available string position
    COPYRA r1
    ADDLA 48
    COPYAR t2
    COPYLR t2 cpy_from
    COPYRR t1 cpy_to
    CALL cpy_ind
    INCR t1
    RETURN


    div:
    # Performs the division Acc/r0
    # Input: 
    #   Acc: int (Dividend)
    #    r0: int (Divisor)
    # Output:
    #   r1:Ratio 
    #   r0:Remainder
    CBR 0 status_reg # Zero bit
    CBR 1 status_reg # Carry bit
    COPYLR 0 r1
    sub_again:
    INCR r1
    SUBRA r0
    # Check if the last SUB hit zero 
    BCRSS 0 status_reg
    JUMP check_carry
    JUMP sub_again
    check_carry:
    # Maybe the last SUB overshot zero
    BCRSS 1 status_reg
    JUMP sub_again
    # Adjust results
    ADDRA r0
    DECR r1
    COPYAR r0
    RETURN

    cpy_ind:
    # Indirect copy
    # Input:
    #   cpy_from: The memory address to copy from
    #     cpy_to: The memory address to copy to
    # Output:
    #   None. The procedure has side effects only
    .DB 7     # Digirule2 ASM COPYRR opcode
    cpy_from:
    .DB 0
    cpy_to:
    .DB 0
    RETURN

    # General Registers
    r0:
    .DB 0
    r1:
    .DB 0
    t0:
    .DB 0
    t1:
    .DB 0
    t2:
    .DB 0

    ascii_str:
    .DB 0,0,0


(This is part of listing :download:`data/math/int2str.dsf <../../data/math/int2str.dsf>` )

The usual workflow is followed to compile it here, assuming that ``dgtools`` is installed already:

::
    
    > dgasm.py int2str.dsf
    > dgsim.py int2str.dgb -ts ascii_str:3

If you now open ``int2str_trace.md`` and scroll all the way to the last step of computation, you will notice the 
ASCII representation of the three bytes starting from memory location `ascii_str`.



Conclusion
----------

This concludes this section on creating a procedure so that we can "see" numbers in a human readable (decimal) 
form.

Although we implemented it for 8bit integers, the function is entirely generic and can be generalised for any size 
integer. That is, as long as the ``div`` function is generalised as well.

The same function can be further generalised to convert integers to a human readable form in other representations 
besides decimal as well. The process is exactly the same, but instead of dividing by powers of 10, we simply divide by 
powers of the base in the desired number system. In fact, this is exactly the way the 
`itoa() <https://en.wikibooks.org/wiki/C_Programming/stdlib.h/itoa>`_ function works.

Finally, as can be seen here, we are starting to set the foundation for a "Super CPU", a CPU that sits on top of
Digirule2 and is capable of more operations (e.g. ``div, mul, int2str``) than the original ASM permits, which in turn
leads to more complex programs.

How about 16bit math next?

