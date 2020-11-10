Super Stack!
============

This section describes the process behind creating a Super Stack! compiler that produces efficient Digirule 2U ASM code. 

If you simply want to know how to compile Super Stack! programs using dgtools, you can jump straight to 
:ref:`compile_sust_dgtools`.

For a brief overview of Super Stack!'s commands, see section :ref:`sust_lang` and 
`this link <https://esolangs.org/wiki/Super_Stack!>`_.

The rest of the sections outline the basic machine that the language targets and how the compiler adapts this "abstract"
machine to the Digirule 2U hardware. 


From brainfuck to Super Stack! 
------------------------------

If you tried to write some programs with brainfuck, you may have found yourself working with data "locally".
That is, even though brainfuck does not impose any restrictions on how exactly memory can be accessed (Random Access), 
memory tends to be accessed in blocks of closely located locations.

Take for example the most elementary computation, that of calculating ``1+1`` (``+>+[-<+>]``). The operands are 
placed on two sequential locations in memory. And when evaluating more complex expressions, with operator precedence 
or brackets, the result of an operation can well be one of the operands of the next operation, therefore, it makes sense 
to keep them close together.

In fact, there is a whole class of computing machines whose operation does not require random memory access at all.

These are the `Stack machines <https://en.wikipedia.org/wiki/Stack_machine>`_.

Stack machines represent yet another model of computation that is **immensely** practical. It therefore made sense to 
try to explore it over a resource constrained CPU system such as the one on the Digirule.

For this purpose, I selected `Super Stack! <https://esolangs.org/wiki/Super_Stack!>`_.

Super Stack! is an esoteric stack based language designed by `Orange <https://esolangs.org/wiki/Super_Stack!>`_. It 
is higher level than brainfuck and closer to more "natural ways" of programming computers. 

This section documents a Super Stack! compiler that reads in Super Stack! and emits the equivalent Digirule Assembly. 

Just as it was done for brainfuck, we first show the basic parts of the "machine" that the language 
assumes and then proceed with the implementation in Digirule ASM and finally an indicative Super Stack! program.


The Super Stack! "system"
-------------------------

A Super Stack! system is composed of Memory, an Arithmetic Logic Unit and basic Input/Output (I/O).


Memory
^^^^^^

Unsurprisingly, all computation in Super Stack! occurs over a memory space that is organised as a stack. 
We have already seen :ref:`how to create a stack and its fundamental operations in Digirule ASM <stack_imp>` and 
there is nothing more to add to that here. 

A stack is treated just like an array, but unlike an array, all operations take place via a ``head_ptr`` (or, head 
pointer) that can only be controlled via two operations and **never** directly:

#. ``Push``, to store a value on the stack
#. ``Pop``, to remove a value from the stack

Both of these operations **always** reference the **top** of the stack, a mode of accessing it that is also known 
as `First In First Out (LIFO) <https://en.wikipedia.org/wiki/Stack_(abstract_data_type)>`_.


Arithmetic Logic Unit
^^^^^^^^^^^^^^^^^^^^^

The Super Stack! system also has an Arithmetic Logic Unit that operates at the top of the stack and can carry out 
the four basic arithmetic operations plus modulo, the two shifts (left and right) and the 3 fundamental logical 
operations. 


Input / Output
^^^^^^^^^^^^^^

And finally, the Super Stack! system can read a value from the input and output a value to the output. This might sound 
similar to brainuck's facilities, *but*, Super Stack! extends those because in addition to ``input, output``, it also 
has commands ``inputascii, outputascii`` and these can be mapped to different "devices" on the 2U Digirule model.


.. _sust_lang:

The Super Stack! language
-------------------------

Super Stack! is not as minimalistic as brainfuck and while "porting" it over to the Digirule, I modified it slightly so 
that it produces more efficient code.

The complete set of commands is as follows:

+------------------------------------------+-------------------------------------------------------------------------+
| Command                                  |   Side effect                                                           |
+==========================================+=========================================================================+
| Any literal BYTE value (1,42,255, etc)   | Immediately pushed on to the stack.                                     |
+------------------------------------------+-------------------------------------------------------------------------+
| **Arithmetic commands**                                                                                            |
+------------------------------------------+-------------------------------------------------------------------------+
| ``add``                                  | Pops two numbers, adds them, *pushes the result on the stack* (ptronts) |
+------------------------------------------+-------------------------------------------------------------------------+
| ``sub``                                  | Pops two numbers, subtracts **the first from the second**, ptronts      |
+------------------------------------------+-------------------------------------------------------------------------+
| ``mul``                                  | Pops two numbers, multiplies them, ptronts.                             |
+------------------------------------------+-------------------------------------------------------------------------+
| ``div``                                  | Pops two numbers, divides **the first by the second**, ptronts          |
+------------------------------------------+-------------------------------------------------------------------------+
| ``mod``                                  | Pops two numbers, performs ``div``, pushes the modulo of that ``div``   |
+------------------------------------------+-------------------------------------------------------------------------+
| ``shl`` (Added in Digirule Super Stack!) | Pops two numbers, shifts the first left by the second bits, ptronts     |
+------------------------------------------+-------------------------------------------------------------------------+
| ``shr`` (Added in Digirule Super Stack!) | Same as ``shl`` but shifts to the right                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| **Logic commands**                                                                                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``and``                                  | Pops two numbers, applies AND, ptronts.                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``or``                                   | Pops two numbers, applies OR, ptronts.                                  |
+------------------------------------------+-------------------------------------------------------------------------+
| ``xor``                                  | Pops two numbers, applies XOR, ptronts.                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``nand``                                 | **Not implemented.** Substitute with ``and 255 xor``                    |
+------------------------------------------+-------------------------------------------------------------------------+
| ``not``                                  | **Not implemented.** Substitute with ``255 xor``                        |
+------------------------------------------+-------------------------------------------------------------------------+
| **Input / Output**                                                                                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``output``                               | Pops the top number sends it to the output followed by a space char.    |
|                                          | **On the Digirule:** Sends the number to the Data Leds.                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``input``                                | Receives a single number from input and push it on the stack.           |
|                                          | **On the Digirule:** Asks for user input from the onboard keyboard.     |
+------------------------------------------+-------------------------------------------------------------------------+
| ``outputascii``                          | Pops the top number and outputs it as an ascii character.               |
|                                          | **On the Digirule:** Sends the number to the serial port                |
+------------------------------------------+-------------------------------------------------------------------------+
| ``inputascii``                           | Receives a string of characters from input and pushes each on the stack | 
|                                          | **backwards**.                                                          |
|                                          | **On the Digirule:** receives a number from the serial port.            |
+------------------------------------------+-------------------------------------------------------------------------+
| **Stack commands**                                                                                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``pop``                                  | Pops the top number and discards it.                                    |
+------------------------------------------+-------------------------------------------------------------------------+
| ``swap``                                 | Swaps the top two numbers.                                              |
+------------------------------------------+-------------------------------------------------------------------------+
| ``cycle``                                | Makes the bottom value of the stack equal to the one at the top of the  | 
|                                          | stack. **Does not pop a value**.                                        | 
+------------------------------------------+-------------------------------------------------------------------------+
| ``rcycle``                               | The opposite of ``cycle`` (the top cell is assigned the bottom cell     | 
|                                          | value). **Does not pop a value**.                                       |
+------------------------------------------+-------------------------------------------------------------------------+
| ``dup``                                  | Duplicates the top number.                                              |
+------------------------------------------+-------------------------------------------------------------------------+
| ``rev``                                  | Reverses the entire stack.                                              |
+------------------------------------------+-------------------------------------------------------------------------+
| **Other commands**                                                                                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``random``                               | Pops the top number, pushes a random number **from 0 to the number      |  
|                                          | popped minus 1**.                                                       |
+------------------------------------------+-------------------------------------------------------------------------+
| ``if``                                   | Equivalent to a ``while`` loop. The conditional is on the top value of  | 
|                                          | the stack. Does not pop the top value.                                  |
+------------------------------------------+-------------------------------------------------------------------------+
| ``fi``                                   | Marks the end of the loop.                                              | 
+------------------------------------------+-------------------------------------------------------------------------+
| ``quit``                                 | Terminates the program.                                                 |
+------------------------------------------+-------------------------------------------------------------------------+
| ``debug``                                | Outputs the entire stack. (Does not pop anything).                      |
|                                          | Not implemented on the Digirule.                                        | 
+------------------------------------------+-------------------------------------------------------------------------+


From Super Stack! to Digirule ASM
---------------------------------

Implementing the Super Stack! "system"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Super Stack! "system" as it was described earlier corresponds to three I/O devices on the Digirule:

#. The keyboard (``input``)
#. The data LEDs (``output``)
#. The Universal Asynchronous Rx/Tx (UART). 
    * That is, the serial port. (``inputascii``, ``outputascii``)

These are all complementary calls and almost identical in structure. For example, the first two expand to:

::

    COPYRR in_dev some_symbol
    
and

::

    COPYRR some_symbol out_dev
    
Where ``in_dev, out_dev`` are the Digirule registers, here defined with dgasm directive ``.EQU`` (see section 
:ref:`sust_prol_epi` for their definition).

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

Transpiling Super Stack! to Digirule ASM is relatively straightforward but slightly more complicated than brainfuck.

This is because, in Super Stack!, a language "symbol" implies a small program composed of more than one ASM instructions
and the way these are pieced together now starts to become an important factor for memory size (and to some extent 
performance).

It would be useful here to further classify Super Stack!'s commands by two key characteristics that help in explaining 
some basic patterns that arise (and that we will exploit). These are:

1. Arity. 
    * `Arity <https://en.wikipedia.org/wiki/Arity>`_ is jargon for "the number of arguments in a function".
2. Stack operation
    * Whether its operation requires a value to be pushed on or poped from the stack.

This classification is as follows:

+---------+-------------------+----------------------------------------------+
| Arity   | Stack operation   | Super Stack! commands                        |
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

And finally, we have the nullary commands. Commands that take no arguments. The result of 
these is independent from the state of the stack. ``quit`` for example will simply interrupt program 
execution and ``rev`` will reverse the stack whether it contains zero or more values.

It is worth showing here very briefly the key idea of the progressive
reductions that these patterns lead us to perform:

The binary functions, conform to :math:`y \leftarrow f(x_1,x_2)` and therefore, in ASM, all end up looking like:

::

    Binary Function Call Pattern:
    
    pop op1
    pop op2
    call binary_function  # Whatever that may be
    push result
    return
        
This pattern *includes* the unary pattern too, where functions look like :math:`y \leftarrow f(x_1)` :

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

In a naive implementation, the program ``[1 1 add 2 sub]`` (or ``1 + 1 - 2``) would include this basic skeleton twice 
when the only difference between the two calls is in just the one line that contains the ``call binary_function`` part. 

To avoid this duplication, we can capture this general pattern in a ``generic_binary`` function whose only parameter 
is which function to call after it has poped two values from the stack. And in doing so, we would also be reducing 
duplication for unary functions, since they are **nested** in the binary pattern.

The same observation holds for nullary functions that *return a result*. These conform to the :math:`y=f()` pattern and 
basically imply just calling the function. In this case however, there is no additional memory saving from 
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
    re-written as ``pop cycle push``, to show that it does not modify the stack, but it would not be wise to implement
    it exactly like this, because calls to ``push`` and ``pop`` are costly.

.. _sust_prol_epi:

Prologue and epilogue parts
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every Digirule transpiled Super Stack! program includes a prologue with all ``.EQU`` directives and the standard 
code that initialises the stack.

Super Stack! programs almost always include some sort of data before commands. For example, to add two numbers the 
Super Stack! code is:

::

    1 1 add quit
    
Normally, the transpiler would emit code to push value 1 to the stack twice. Instead of wasting memory for this "setup" 
code, the transpiler catches this "pattern" and simply pre-loads the stack with data.

Finally, the epilogue part includes declarations for setting up the stack, its head pointer and concatenating together 
the "dependencies" imposed by commands earlier in the program (e.g. the sub-routines that implement the Super Stack! 
functions).


Handling errors
~~~~~~~~~~~~~~~

What happens if we try to pop the empty stack or push on to a full stack?

Very bad things. The way programs are laid out in the 256 bytes of memory is to place the code first, followed by the 
stack memory space, followed by the memory mapped devices. Therefore, any unchecked underflow would start erasing code 
and similarly any unchecked overflow would overwrite the status register which usually holds temporary state for 
iterations.

To avoid this, both the ``f_push`` and ``f_pop`` operations perform checks before carrying out their operation and 
never allow the stack to over or under flow. This error condition is handled by ``f_stack_error`` which simply
turns the data LEDs on and stops the execution of the program. ``f_stack_error`` is included  along with a typical 
``f_push, f_pop`` pair forming the block:

::

    f_push:
    COPYRA head_ptr
    SUBLA 253
    BCRSC zero_bit status_reg
    JUMP f_stack_error
    COPYRI head_val head_ptr
    INCR head_ptr
    RETURN

    f_pop:
    COPYRA head_ptr
    CBR carry_bit status_reg
    SUBLA stack
    BCRSC zero_bit status_reg
    JUMP f_stack_error
    DECR head_ptr
    COPYIR head_ptr head_val
    RETURN

    f_stack_error:
    COPYLR 0xFF out_dev
    JUMP f_stack_error



Putting it all together
-----------------------

Here is the general skeleton of a Super Stack! program transpiled in Digirule ASM:

::

    # PROLOGUE
    # Sets up basic symbols and the stack
    
    .EQU status_reg=252
    .EQU in_dev=253
    .EQU out_dev=255
    .EQU zero_bit=0
    .EQU carry_bit=1
    COPYLR stack_offset head_ptr    # Initialise stack
    
    # MAIN PROGRAM
    start_program:
    ...
    ...
    HALT
    
    # SUB-ROUTINES
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
    ...
    f_custom_ins:
    .DB 0
    # INTERNAL TEMPORARY REGISTERS / COMMAND ARGUMENTS
    head_val:
    .DB 0
    head_val_1:
    .DB 0
    RETURN
    
    # STACK
    head_ptr:         # The head pointer keeps track of the top of the stack
    .DB 0
    stack:
    .DB 1,2
    stack_offset:     # stack_offset is a label and at program initialisation always points at the end of the stack.



.. _compile_sust_dgtools:

Using `dgtools` to compile Super Stack! programs
------------------------------------------------

The Super Stack! compiler is called :ref:`dgsust <dgsust_desc>` and produces a Digirule Assembly source code file 
(a `.dsf`) that is then compiled to an executable by `dgasm`. 

``dgsust`` accepts a single filename and produces output right through ``stdout``.

Given the Super Stack! code in some file ``sust_code.ssf``, a typical command line session goes like this:

::

    \> dgsust.py sust_code.ssf>asm_code.dsf    # Super Stack! --> Assembly
    \> dgasm.py asm_code.dsf -g 2U             # Assembly --> Executable (Notice that the target is 2U)
    \> dgsim.py asm_code.dgb -I                # Simulation
    \> xdg-open asm_code_trace.html            # Output
    

.. note::
    Notice how ``dgsim.py`` was called with ``-I``, putting it in interactive mode. 
    This is necessary only if your program contains the 4 I/O commands and you would like to 
    really try entering different numbers yourself. If ``-I`` is not provided, then 
    ``dgsim.py`` will ignore the I/O commands.

For more information on compiling Digirule ASM programs in general, see :ref:`here <intro-topics>`.

Let's try this with a simple program.


``Hello World`` in Super Stack!
-------------------------------

Most ``hello world`` programs are just that: A snippet of code that outputs that phrase. This is possible on the 
Digirule 2U, but frankly, quite boring. All that you do is load a bunch of bytes on the stack and shift them out to the 
serial interface.

Instead, just as it was done for brainfuck,  we are taking a different approach, demonstrating addition. The following 
program accepts two numbers from the user, adds them and turns the data LEDs on.

In Super Stack! :

::

    input   # Reads a value from the keyboard and pushes it on the stack
    input   # Repeats the above
    add     # Pops the top two values, adds them and puses the result on 
            # to the stack
    output  # Pops the top value and sends it to the data LEDs
    quit

This is compiled down to Digirule ASM as:

.. literalinclude:: ../../dg_asm_examples/superstack/add_two_nums.dsf
    :language: DigiruleASM
    :linenos:



Conclusion
----------

Super Stack! captures the simplicity and power of stack based computing and is a perfect fit for programming on  
resource constrained CPUs such as the Digirule.

Although it is an "esolang", it is already very close to a usable language. With a little bit of effort we can turn 
the ``if, fi`` pair to an ``if [run this] else [run this] fi`` kind of construct. And with a little bit more effort we 
can add the ability to work with references so that we can push arbitrary values from anywhere in memory on to the stack.
And at that point, we would also be able to "tag" a certain portion of the stack with a symbol so that when it is 
next "seen", it executes that portion of the stack. This would then pave the way for the ability to write arbitrary 
precision arithmetic functions and to an extent introduce rudimentary "data types".

But if we did all this, we would have then derived `Forth <https://en.wikipedia.org/wiki/Forth_(programming_language)>`_, 
out of Super Stack!
