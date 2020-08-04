A Superstack compiler for Digirule
==================================

Along with Brainfuck, Superstack is another one of those "esoteric" programming languages.

The motivation for creating a compiler for it was two-fold:

#. Stack machines represent yet another model for computation.
#. Operations over a stack are very important for evaluating mathematical expressions.


The Superstack "system"
-----------------------

Unsurprisingly, given its name, all computation in Superstack occurs over a stack. We have already seen 
:ref:`how to create a stack and its fundamental operations before <stack_imp>` and there is nothing more to add here.

A stack is treated just like an array, but unlike an array, all operations take place via a ``head_ptr`` (or, head 
pointer). Consequently, the stack data structure is updated via two operations:

#. ``Push``, to extend the stack by a value
#. ``Pop``, to remove a value from the stack

Again, both of these operations **always** referencing the top of the stack.

The Superstack system also has an Arithmetic Logic Unit which operates over the top of the stack and can carry out 
the four basic arithmetic operations (plus modulo) and the 3 basic logical operations. 

And finally, the Superstack can read a value from the input and output a value to the output. This might sound similar 
to Brainuck's facilities, *but*, Superstack extends those because in addition to ``input, output``, it also has commands 
``inputascii, outputascii`` and these can be mapped to different "devices" on the 2U Digirule model.


The Superstack Language
-----------------------

Superstack is not as minimalistic as Brainfuck and while "porting" it over to the Digirule, I modified it slightly.
The complete set of commands is as follows:

+----------------------------------------+-------------------------------------------------------------------------+
| Command                                |   Side effect                                                           |
+========================================+=========================================================================+
| Any literal BYTE value (1,42,255, etc) | Immediately pushed on to the stack.                                     |
+----------------------------------------+-------------------------------------------------------------------------+
| **Arithmetic commands**                                                                                          |
+----------------------------------------+-------------------------------------------------------------------------+
| ``add``                                | Pops two numbers, adds them, *pushes the result on the stack* (ptronts) |
+----------------------------------------+-------------------------------------------------------------------------+
| ``sub``                                | Pops two numbers, subtracts **the first from the second**, ptronts      |
+----------------------------------------+-------------------------------------------------------------------------+
| ``mul``                                | Pops two numbers, multiplies them, ptronts.                             |
+----------------------------------------+-------------------------------------------------------------------------+
| ``div``                                | Pops two numbers, divides **the first by the second**, ptronts          |
+----------------------------------------+-------------------------------------------------------------------------+
| ``mod``                                | Pops two numbers, performs ``div``, pushes the modulo of that ``div``   |
+----------------------------------------+-------------------------------------------------------------------------+
| **Logic commands**                                                                                               |
+----------------------------------------+-------------------------------------------------------------------------+
| ``and``                                | Pops two numbers, applies AND, ptronts.                                 |
+----------------------------------------+-------------------------------------------------------------------------+
| ``or``                                 | Pops two numbers, applies OR, ptronts.                                  |
+----------------------------------------+-------------------------------------------------------------------------+
| ``xor``                                | Pops two numbers, applies XOR, ptronts.                                 |
+----------------------------------------+-------------------------------------------------------------------------+
| ``nand``                               | **Not implemented.** Substitute with ``and 255 xor``                    |
+----------------------------------------+-------------------------------------------------------------------------+
| ``not``                                | **Not implemented.** Substitute with ``255 xor``                        |
+----------------------------------------+-------------------------------------------------------------------------+
| **Input / Output**                                                                                               |
+----------------------------------------+-------------------------------------------------------------------------+
| ``output``                             | Pops the top number sends it to the output followed by a space char.    |
|                                        | **On the Digirule:** Sends the number to the Data Leds.                 |
+----------------------------------------+-------------------------------------------------------------------------+
| ``input``                              | Receives a single number from input and push it on the stack.           |
|                                        | **On the Digirule:** Asks for user input from the onboard keyboard.     |
+----------------------------------------+-------------------------------------------------------------------------+
| ``outputascii``                        | Pops the top number and outputs it as an ascii character.               |
|                                        | **On the Digirule:** Sends the number to the serial port                |
+----------------------------------------+-------------------------------------------------------------------------+
| ``inputascii``                         | Receives a string of characters from input and pushes each on the stack | 
|                                        | **backwards**.                                                          |
|                                        | **On the Digirule:** receives a number from the serial port.            |
+----------------------------------------+-------------------------------------------------------------------------+
| **Stack commands**                                                                                               |
+----------------------------------------+-------------------------------------------------------------------------+
| ``pop``                                | Pops the top number and discards it.                                    |
+----------------------------------------+-------------------------------------------------------------------------+
| ``swap``                               | Swaps the top two numbers.                                              |
+----------------------------------------+-------------------------------------------------------------------------+
| ``cycle``                              | Makes the bottom value of the stack equal to the one at the top of the  | 
|                                        | stack. **Does not pop a value**.                                        | 
+----------------------------------------+-------------------------------------------------------------------------+
| ``rcycle``                             | The opposite of ``cycle`` (the top cell is assigned the bottom cell     | 
|                                        | value). **Does not pop a value**.                                       |
+----------------------------------------+-------------------------------------------------------------------------+
| ``dup``                                | Duplicates the top number.                                              |
+----------------------------------------+-------------------------------------------------------------------------+
| ``rev``                                | Reverses the entire stack.                                              |
+----------------------------------------+-------------------------------------------------------------------------+
| **Other commands**                                                                                               |
+----------------------------------------+-------------------------------------------------------------------------+
| ``random``                             | Pops the top number, pushes a random number **from 0 to the number      |  
|                                        | popped minus 1**.                                                       |
+----------------------------------------+-------------------------------------------------------------------------+
| ``if``                                 | Equivalent to a ``while`` loop. The conditional is on the top value of  | 
|                                        | the stack. Does not pop the top value.                                  |
+----------------------------------------+-------------------------------------------------------------------------+
| ``fi``                                 | Marks the end of the loop.                                              | 
+----------------------------------------+-------------------------------------------------------------------------+
| ``quit``                               | Terminates the program.                                                 |
+----------------------------------------+-------------------------------------------------------------------------+
| ``debug``                              | Outputs the entire stack. (Does not pop anything).                      |
|                                        | Not implemented on the Digirule.                                        | 
+----------------------------------------+-------------------------------------------------------------------------+


From SuperStack to Digirule ASM
-------------------------------

Implementing the Superstack "system"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Transpiling the commands
^^^^^^^^^^^^^^^^^^^^^^^^

Prologue and epilogue parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Putting it all together
-----------------------

