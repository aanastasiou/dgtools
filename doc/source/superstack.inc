A Superstack compiler for Digirule
==================================

Along with Brainfuck, Superstack is another one of those "esoteric" programming languages.

The motivation for creating a compiler for it was two-fold:

#. Stack machines represent yet another model for computation.
#. Operations over a stack are very important for evaluating mathematical expressions.

Just as it was done for Brainfuck, this section first shows the basic parts of the "machine" that the language 
assumes and then proceeds with their implementation in Digirule ASM and finally some indiciative superstack programs.


The Superstack "system"
-----------------------

Unsurprisingly, given its name, all computation in Superstack occurs over a stack. We have already seen 
:ref:`how to create a stack and its fundamental operations before <stack_imp>` and there is nothing more to add here.

A stack is treated just like an array, but unlike an array, all operations take place via a ``head_ptr`` (or, head 
pointer). Consequently, the stack data structure is updated via two operations:

#. ``Push``, to extend the stack by a value
#. ``Pop``, to remove a value from the stack

Again, both of these operations **always** reference the top of the stack.

The Superstack system also has an Arithmetic Logic Unit which operates over the top of the stack and can carry out 
the four basic arithmetic operations (plus modulo), the two shifts (left and right) and 3 basic logical operations. 

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
| Any literal BYTE value (1,42,255, etc) | Immediately pushed on to the stack. Equivalent to ``NUM push``          |
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
| ``shl`` (Added in Digirule SuperStack) | Pops two numbers, shifts the first left by the second bits, ptronts     |
+----------------------------------------+-------------------------------------------------------------------------+
| ``shr`` (Added in Digirule SuperStack) | Same as ``shl`` but shifts to the right                                 |
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

The Superstack "system" as it was described earlier corresponds to three I/O devices on the Digirule:

#. The keyboard (``input``)
#. The data LEDs (``output``)
#. The Universal Asynchronous Rx/Tx (UART). That is, the serial port. (``inputascii``, ``outputascii``)

These are all complementary calls and almost identical in structure. For example, the first two expand to:

::

    COPYRR in_dev some_symbol
    
and

::

    COPYRR some_symbol out_dev
    
Where ``in_dev, out_dev`` are the Digirule registers, here defined with dgasm directive ``.EQU``.

Similarly, the ascii counterparts expand to:

::

    COMIN
    COPYAR some_symbol
    
and

::

    COPYRA some_symbol
    COMOUT
    
Where ``some_symbol`` is a one byte memory location.


Transpiling the commands
^^^^^^^^^^^^^^^^^^^^^^^^

Transpiling superstack to Digirule ASM is relatively straightforward but slightly more complicated than Brainfuck.

This is because, in Superstack, a language "symbol" implies a small program composed of more than one ASM instructions
and the way these are pieced together now starts to become an important factor for memory size (and to some extent 
performance).

It would be useful here to further classify Superstack's commands by arity because it will help in explaining some 
basic patterns that arise. Arity is jargon for "the number of arguments in a function".

This classification is as follows:

+---------+-------------------+----------------------------------------------+
| Arity   | Stack operation   | Superstack commands                          |
+=========+===================+==============================================+
| Nullary |  PUSH             | ``input``, ``inputascii``                    |       
|         +-------------------+----------------------------------------------+
|         |  POP              | ``pop``                                      |
|         +-------------------+----------------------------------------------+
|         |  NONE             | ``rev``, ``quit``                            |
+---------+-------------------+----------------------------------------------+
|  Unary  |  PUSH             | ``push (literal)``                           |       
|         +-------------------+----------------------------------------------+
|         |  POP              | ``output``, ``outputascii``, ``dup``         |
|         +-------------------+----------------------------------------------+
|         |  NONE             | ``random``, ``cycle``, ``rcycle``, ``if/fi`` |
+---------+-------------------+----------------------------------------------+
| Binary  |  PUSH             |                                              |
|         +-------------------+ ``shl``, ``shr``, ``add``, ``sub``, ``mul``, |
|         |  POP              | ``div``, ``mod``, ``and``, ``or``, ``xor``,  |
|         |                   | ``swap``                                     |
|         +-------------------+----------------------------------------------+
|         |  NONE             |                                              |
+---------+-------------------+----------------------------------------------+

The vast majority of commands are binary, requiring two operands they receive from the stack and pushing one result 
back on to the stack.

These are followed, in number of commands, by the unary ones. These require only one operand and their structure is 
exactly the same as above but only consisting of a single pop. 

And finally, we have the nullary commands. The result of 
these functions is independent from the state of the stack. ``quit`` for example will simply interrupt program 
execution and ``rev`` will reverse the stack whether it contains zero or more values.

Although the optimisation process was incremental, it is worth showing here very briefly the key idea of the progressive
reductions that were applied to the code.

The binary functions, conform to :math:`y = f(x_1,x_2)` and therefore, in ASM, all end up looking like:

::
    Binary Function Call Pattern:
    
    pop op1
    pop op2
    call binary_function
    push result
    return
        
This pattern *includes* the unary pattern, where functions look like :math:`y=f(x_1)`, too:

::

    Binary / Unary Function Call Pattern:
    
    binary:
    pop op1
    unary:
    pop op2
    call binary_unary_function
    push result
    return
    
And finally, we have the nullary functions and those unary ones that do not receive any parameters from the stack, 
**but** do return values on it.

In a naive implementation, the program ``[1 1 add 2 sub]`` (or ``1 + 1 - 2``) would include this pattern twice when
the only difference between the two calls is the ``call binary_function`` part. 

To avoid this duplication, we can capture this general pattern in a ``generic_binary`` function whose only parameter 
is which function to call after it has poped two values from the stack. And in doing so, we would also be reducing 
duplication for unary functions, since they are **nested** in the binary pattern.

The same observation holds for nullary functions that *return a result*. These conform to the :math:`y=f()` pattern and 
basically imply simply calling the function. In this case however, there is no additional memory saving from 
embeding them one level down in the *Binary/Unary* function pattern. This is because a call to *Binary/Unary* costs 
5 bytes: 3 bytes to set the ``binary_unary_function`` it needs to call and 2 bytes to make the call. 








For example, the general call to ``add`` is translated to:

::

    COPYLR f_add f_custom_ins
    CALL f_pop_call_push        # This initiates a call to ``add``
    
    ...
    f_pop_call_push:
    CALL f_pop
    f_call_push:
    CALLI f_custom_ins
    CALL f_push
    RETURN
    
    ...
    
    f_add:
    CALL f_preamble
    COPYRA head_val_1
    CBR carry_bit status_reg
    ADDRA head_val
    COPYAR head_val
    RETURN
    
    ...
    
    f_preamble:
    COPYRR head_val head_val_1
    CALL f_pop
    RETURN

Similarly, a call to a unary command first pops a single value and then calls the function and finally, nullary commands
are simply called directly.

.. note::
    You might notice here that ``cycle`` is included in the unary commands, although calling ``cycle`` does not require
    that a value is poped. However, as a function, ``cycle`` requires one parameter from the stack. It could be 
    re-written as ``pop cycle push``, to show that it does not modify the stack, but it could not be implemented like 
    this, because calls to ``push`` and ``pop`` are costly.


Prologue and epilogue parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every Digirule transpiled Superstack program includes a prologue with all ``.EQU`` directives and the standard 
initialisation of the stack.

Superstack programs almost always include some sort of data before commands. For example, to add two numbers the 
superstack code is:

::

    1 1 add quit
    
Normally, the transpiler would emit code to push value 1 to the stack twice. Instead of wasting memory by emitting code 
for pushing values, the transpiler catches this condition and simply pre-loads the stack with data.

Finally, the epilogue part includes declarations for setting up the stack, its head pointer and concatenating together 
the "dependencies" imposed by commands earlier in the program (e.g. the sub-routines that implement the Superstack 
functions).

Putting it all together
-----------------------

Here is the general skeleton of a Superstack program transpiled in Digirule ASM:

::

    .EQU status_reg=252
    .EQU in_dev=253
    .EQU out_dev=255
    .EQU zero_bit=0
    .EQU carry_bit=1
    COPYLR stack_offset head_ptr    # Initialise stack
    start_program:
    ...
    ...
    HALT
    f_add:
    CALL f_preamble
    COPYRA head_val_1
    CBR carry_bit status_reg
    ADDRA head_val
    COPYAR head_val
    RETURN
    f_sub:
    ...
    ...
    f_pop_call_push:
    CALL f_pop
    f_call_push:
    CALLI f_custom_ins
    CALL f_push
    RETURN
    f_custom_ins:
    .DB 0
    head_val:
    .DB 0
    head_val_1:
    .DB 0
    RETURN
    head_ptr:
    .DB 0
    stack:
    .DB 1,2
    stack_offset:
