.. _lfsr:

Pseudorandom Number Generator (PRNG)
====================================

The availability of random numbers in modern computers is taken for granted. 
We always assume that it will be possible to simulate the throw of a dice by 
calling a function that "magically" returns a random number.


But, where do random numbers come from and how can we use the Digirule2 to 
generate a few?

The Linear Feedback Shift Register (LFSR)
-----------------------------------------

This section demonstrates a very simple, but effective technique of producing a series of random numbers using 
Digirule2 ASM. This technique is based on a "shift register" and it does not really have to be implemented in 
software since it is possible to build it on a breadboard out of discrete components or even program it on a 
Field Programmable Gate Array (FPGA).

Its operation is very simple, an exclusive OR (XOR) function over the current binary number stored in the register is 
used to produce a 0/1 result. Then, the bits in the register are shifted to the right and the XOR result is sent to 
the Most Significant Bit (MSB) of the register. This process is repeated, each time taking the shift register from 
one state to the next. The shift direction and whether the new bit is added at the MSB or Least Significant Bit (LSB) 
sides are of course interchangeable.

Obviously, there is nothing truly "random" in this process. But given a long enough shift register and a carefully 
chosen combination of its output to be XORed, the amount of different states the register goes through is so large that 
they appear to be random, especially to a human being.

A PRNG based on this technique is called a *"Linear Feedback Shift Register"*. It is Linear, because the
calculation of the new bit is a linear combination of the outputs of the shift register. It uses "Feedback" because 
the bit derived from the current state of the register is sent back through the same register. And finally, it is 
called "Shift Register" because at each step, the register is shifted either to the left or the right to "make space"
for the calculated bit.

Two variants of this are presented here: an 8bit PRNG and a 9bit PRNG.

An 8bit PRNG
------------

As explained in the brief introduction about LFSRs, there are two things that need to be managed, the "width" of the 
shift register and which outputs are to be combined in order to produce the feedback bit. Both of these parameters 
determine the "randomness" of the generator.

Considering the width of the shift register is straightforward: An :math:`N` bit shift register is capable of producing 
:math:`2^{N-1}` states. An 8bit PRNG is expected to produce 255 different numbers before running out of combinations 
and repeating itself. Similarly a 64bit PRNG is expected to produce **18,446,744,073,709,551,615** combinations, before
repeating itself.

Repetition is not good for randomness but this is why these are called "Pseudo-random" generators. 

But, considering which outputs of the register to combine, so that the shift register goes through all of its possible 
states, is a more difficult problem. For example, you may have noticed that the shift register never goes through 
the all-zeros state (hence the :math:`N-1` above). If the LFSR ever hits the all-zeros state it will never move out 
of it. This is because of the truth table of the XOR function where zeros at both of its inputs result in a zero at its 
output. It is only if (and only if) either of its inputs is 1, that the output of the XOR equals a logic 1 too. This 
means that the inputs must be chosen carefully, otherwise they might put the state register through a much shorter and 
predictable cycle of numbers that would not appear random at all.

Fortunately, the rules behind the selection of the right outputs so that an :math:`N` bit LFSR really does go through 
all of its states have been worked out and `the Wikipedia webpage on 
LFSRs <https://en.wikipedia.org/wiki/Linear-feedback_shift_register>`_ includes them in a table, with one combination
per value of :math:`N`, from a mere 2bit LFSR all the way to 24 and beyond.

For :math:`N=8`, the "polynomial" that describes which inputs to be used in the calculation of the feedback bit is:

.. math::

    x^8 + x^6 + x^5 + x^4 + 1
    
In this case, the shift register is shift to the right and :math:`x^8` is the input. Bit positions are counted **from
the left**.

Therefore, all that we have to do here is grab a bunch of bits, XOR them, shift the register and send the calculated bit
at its input.

This is a one liner in Python:

.. code :: Python

    # Remember here, bit positions are counted from the left.
    # x>>2 is x^4, x>>3 is x^5 and so on.
    rn=lambda x:(x>>1) | (((x ^ (x>>2) ^ (x>>3) ^ (x>>4)) & 1)<<7)
    
    print(rn(42)) # Returns 149
    print(rn(rn(42))) # Returns 202 and so  on


The evaluation of this one liner in Digirule2 ASM proceeds as follows:

.. code-block:: DigiruleASM
    :linenos:
    :name: lfsr8bit

    .EQU status_reg=252
    .EQU carry_bit=1
    
    COPYRA state
    COPYRR state R1
    SHIFTRR state
    CBR carry_bit status_reg
    SHIFTRR state
    XORRA state
    CBR carry_bit status_reg
    SHIFTRR state
    XORRA state
    CBR carry_bit status_reg
    SHIFTRR state
    XORRA state
    ANDLA 1
    COPYAR R2
    CBR carry_bit status_reg
    SHIFTRR R1
    DECRJZ R2
    JUMP clr_bit
    set_bit:
    SBR 7 R1
    JUMP resume
    clr_bit:
    CBR 7 R1
    resume:
    COPYRR R1 state
    HALT
    state:
    .DB 42
    R1:
    .DB 0
    R2:
    .DB 0
    
This is part of :download:`../../dg_asm_examples/lfsr/lfsr.dsf`

Notice here that in the first two operations, the current state is saved in ``R1`` and then undergoes a series of 
shifts and XORs between these shifted versions. The ``CBR`` that precedes the SHIFT is specific to Digirule2 ASM because 
its shift operation is through the Carry bit. Also, although the whole word is XORed, we are only interested in the LSB.
Finally, the input bit of the shift register (the :math:`x^8`) is set (or cleared) and the final value is copied back 
to the state register.

To this, we can also add an array, as demonstrated in section :ref:`advanced-topics` and add another parameter that 
controls the maximum number of numbers to generate.

With an initial state value of :math:`42` and set to produce 10 random numbers, this program returns:

``149, 202, 229, 114, 185, 220, 238, 119, 187, 221``


Putting it all together
-----------------------

The complete listing is as follows:


.. literalinclude:: ../../dg_asm_examples/lfsr/lfsr.dsf
    :language: DigiruleASM
    :linenos:



1bit Powerup! - A 9bit PRNG!
----------------------------

Surprisingy, a 9bit PRNG is not only feasible on the Digirule2, it probably runs faster than the 8bit but 
if it was to be used practically, it ends up being inefficient.  

The technique is exactly the same but in the case of the 9bit PRNG we are taking into advantage the fact that the 
``SHIFT**`` operations are *through carry* on the Digirule2. Therefore, 1 more bit is inserted in the 
whole process, for free.

This characteristic, along with the fact that the 9bit PRNG uses a 2 factor polyonym, makes this PRNG much faster 
compared to the 8bit version.

The only problem with this version however is that if this PRNG was to be packaged in a re-usable form, then both 
the ``state`` variable as well as the Carry flag bit (that is 1 bit) would have to be stored and re-stored between 
calls to the function. Since it is impossible to save a single bit, two bytes would have to be used. Out of these 
two bytes, the second one would practically be going "to waste".

Here is what this implementation looks like:

.. literalinclude:: ../../dg_asm_examples/lfsr/lfsr_9bit.dsf
    :language: DigiruleASM
    :linenos:


Notice here that due to the fact that only 1 XOR is required, it is run "in-place" through a series of bit tests that 
directly modify the Carry flag, prior to shifting the register.

As before, we get to see only the lower 8bits but with much more variation in the available combinations. This routine
produces these numbers: ``149, 202, 229, 114, 185, 220, 238, 119, 187, 221``

The complete listing adds parameters for the initial state of the register and how many numbers to generate and is 
available in :download:`../../dg_asm_examples/lfsr/lfsr_9bit.dsf`

Conclusion
----------

Providing the ability to generate random numbers on the Digirule2 means that we can now set new "random" objectives in 
games.

For example, one of the Digirule2 demos is a game of "Guess the number", where the player tries to guess a hidden number
in as few guesses as possible. 

With a random number generator, it is now possible to make the game restart, with a new unknown number challenge 
for the player, or have the :ref:`pov_light_stick` display random "images".
