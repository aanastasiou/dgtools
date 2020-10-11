Brainfuck
=========

What is Brainfuck? Why would anyone want to learn Brainfuck? Why would anyone waste their time with Brainfuck? 
What does Brainfuck have to do with retrocomputing and the Digirule?

A very brief introduction
-------------------------

Brainfuck is a Turing complete language with just 8 commands that operate on an array of bytes of finite size. 

Stating that a particular "machine" is `Turing complete <https://en.wikipedia.org/wiki/Turing_completeness>`_ implies 
that *anything that is computable*, can be computed with it. And, stating that this "machine" can achieve this with 
just 8 commands and some memory implies that computation, *any computation*, can be broken down into this minimal set 
of fundamental operations. 

In other words, taken to the extreme, it **is** possible to write a Brainfuck program that implements 
something like an `iterative approximation to finding the square root of a number <https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method>`_, 
or something like `"World of Warcraft" <https://en.wikipedia.org/wiki/World_of_Warcraft>`_. 

It is not going to be easy. It is not going to be human readable or easy to debug and follow.

But it **is**, provably, doable.

Brainfuck was conceived by `Urban Dominic Muller <https://www.youtube.com/watch?v=gjm9irBs96U&feature=youtu.be&t=8722>`_ 
in the early 90s while he was the administrator of `Aminet <http://wiki.aminet.net/index.php/The_history_of_Aminet>`_, 
the largest software repository of Amiga sofware in the world. Muller was inspired by an earlier language 
(`FALSE <http://progopedia.com/language/false/>`_) and both that one and Brainfuck had the same key objective: 
To be compiled to a program with as small a compiler as possible.

These reasons, already make Brainfuck worth a second look, outside the context of an Assembly demo, such as the others 
that are available here.

However, my basic motivation when writing the Brainfuck compiler was to use it as a very small and self contained 
example of a way of thinking about CPUs, computers and hardware. Sure, we could sit here and write ASM programs that 
do *stuff*, in 256 bytes for data and code, for ever. But soon enough, we find ourselves repeating 
ref:`the same small set of basic techniques <vol_0>` of structuring the Assembly instructions of the CPU. Wouldn't it 
be nicer, to be able to tell the CPU what we want it to do at a higher level?

Brainfuck does exactly that and is incredibly simple to parse and generate programs for.

There are a tonne of Brainfuck compilers out there. And if you think of a compiler itself as a computation process, 
there are even Brainfuck interpreters. That is, programs written in Brainfuck that 
*accept a Brainfuck program and re-produce its result*. 

Modern Brainfuck compilers can be created with a size very close to the total memory of a machine such as the Digirule 
(256 bytes) when written in ASM.

But since we have to fit **both** data **and** code in the span of 256 bytes, it was looking as if a compiler that reads 
Brainfuck and produces Digirule Assembly was more suitable for this goal.

And with this, the objective was set: *"Is it possible to write a Brainfuck compiler for the Digirule?"*

Because, if it is possible, then this means that we can "ignore" the tens of instructions in the Digirule instruction 
set and achieve the same outcome with just the 8 Brainfuck instructions.

Needless to say, if you have reached this point, that it **is** possible. And given the proliferation of computer 
languages, compilers, transpilers, etc, it is not even a "new" idea.

It is however fun to have done and if you are interested in finding out more about how it works keep reading. 

Alternatively, you can simply jump to the practical section that outlines the Brainfuck programs you can use with 
the Brainfuck compiler.




The Brainfuck "System"
----------------------

Brainfuck, as a language, is associated with an underlying machine that is very close, in form, to the Turing Machine.

The layout of this "machine" explains directly the instruction set.


The machine
^^^^^^^^^^^

Brainfuck targets a "machine" that is composed of the following peripherals:

1. A "tape", which is an ancient word for "memory" or "an array of numbers"
2. A "Data Pointer" (DP) that points to some point on the tape. This is quite simply the index within the array 
   of numbers. 
3. An Arithmetic Logic Unit (ALU) that can only add and subtract **by one**
4. An input device; and 
5. An output device.


The instruction set
^^^^^^^^^^^^^^^^^^^

These "peripherals" are the targets of its extremely small and simple instruction set. This is as follows: 

+-----------+-------------------------------------------------------------------------------------------------------------+
|  Command  |  Result                                                                                                     |
+===========+=============================================================================================================+
|   ``>``   | Increase the DP by one (it now points to the next cell)                                                     |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``<``   | Decrease the DP by one (it now points to the previous cell)                                                 |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``+``   | Increase the **memory value** that the DP points to by one                                                  |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``-``   | Decrease the **memory value** that the DP points to by one                                                  |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``.``   | Send the **memory value** that the DP points to, to the output                                              |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``,``   | Accept some input and store it to the current place the DP points to                                        |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``[``   | If the current memory value at the DP is zero jump over any commands within the matching pair of ``[]``     |
+-----------+-------------------------------------------------------------------------------------------------------------+
|   ``]``   | If the current memory value at the DP is non-zero jump back to the first command within the matching ``[]`` |
+-----------+-------------------------------------------------------------------------------------------------------------+


At this point, it might be tempting to start piecing these little atoms (the instructions) together, to form bigger 
molecules (programs, libraries, etc).

Bear with me here however, because we will soon be writing Brainfuck programs that execute on the Digirule.


From Brainfuck to Digirule ASM
------------------------------

Implementing the machine
^^^^^^^^^^^^^^^^^^^^^^^^

A Brainfuck memory "tape" is quite simply an array. An array in Digirule Assembly can be represented by a base memory 
address (the start of the array) and an offset to a particular memory cell. Let's call this array...``tape``. 

If you would like to catch up with representing arrays in ASM and Digirule ASM in particular, you might want to see 
:ref:`this first <array_indexing>`

Having defined the array, we also need to define its offset. Notice here that in Brainfuck, the offset to the 
memory is the "Data Pointer". So, let's define a "variable" called ``dp``, representing the current position within the 
array.

If you would like to catch up with plain simple operations (such as assignments) in Digirule ASM, you might want to see 
:ref:`this first <assignments>`.

Modelling the input and output devices is also easy. On the Digirule, these can be mapped directly to the "keyboard" 
and data led display "peripherals". Both look like simple data transfers between memory locations.


Transpiling the commands
^^^^^^^^^^^^^^^^^^^^^^^^

With very little overhead, it is possible to map the Brainfuck commands to Digirule (2U) assembly. This will be 
demonstrated here by walking through the implementation of three commands: 

#. The "Move Right" (``>``)
#. The "Add 1" (``+``); and
#. The "Iteration" (``[ ]``).

The first two, are basically the same side effect (increase a "value") but towards different targets. To "move right" 
we simply need to add 1 to the ``dp``. To increase the value that the ``dp`` points at, we need to add one to where it 
points to.

The naive implementation of the first is:

::

    INCR dp
    
However, notice that Brainfuck does not have literals. In plain simple Brainfuck, it is impossible to specify ``12`` 
as the value somewhere along the "tape". So, the literal ``12``, in Brainfuck is ``++++++++++++`` which leads 
to adding 12 units to the initial value of the memory tape cell. The 
naive implementation therefore, leads to 12 calls to ``INCR`` and more generally :math:`\text{reps} \times 2` 
bytes of memory. Here, :math:`\text{reps}` stands for the number of times the ``+`` symbol appears at a 
specific point in the input program.

For this reason, the Brainfuck transpiler, "catches" the repeated application of ``+ - > <`` and converts them to the 
more efficient:

::

    COPYRA dp
    ADDLA {reps}
    COPYAR dp
    
Where ``{reps}`` is the number of times the symbol appears in the input. 

This is just 6 bytes in Digirule ASM. The converse command (``<``) has ``SUBLA`` in the place of ``ADDLA``.

Similarly, adding 1 to the value of where the ``dp`` points to, is a matter of executing the same commands **but**, over 
the value the ``dp`` points at.

Unfortunately, an indirect ``INCR`` is impossible with the "2U" Digirule firmware, which means that it would have to be 
done via the usual :ref`way of building up the instruction at runtime <iset_notes_mem_ops>`:

::

    ...
    COPYLR 30 handle_dv_i
    CALL handle_dv_i
    ...
    ...
    handle_dv_i:
    .DB 0
    dp:
    .DB 0
    RETURN
    tape:
    ...

Notice here how the ``dp`` is between the instruction ``handle_dv_i`` and a byte for ``RETURN`` that is required 
to return from the indirect ``INCR``. The combined result of this is to increase the value that the ``dp`` points to.

Adding an arbitrary :math:`\text{reps}` number involves less steps since the 2U firmware now has indirect copy 
instructions at least, *but*, it also requires the addition of a ``CBR`` because the ``ADD`` now is with-carry:

::

    COPYIA dp
    CBR carry_bit status_reg
    ADDLA {reps}
    COPYAI dp
    

Finally, the iteration is equivalent to the usual ``while``. In other words, check a condition and execute the loop 
until that condition does not hold.

We have :ref:`seen how conditional branching works before <cond_branch>`, already using the 2A firmware and the 
implementation of ``while`` is exactly the same thing with a bit more label management.

Here is how a given pair of ``[ ]`` containing the block of instructions to be executed, would be transpiled:

::
    label_216276956994:
    COPYIA dp
    BCRSC zero_bit status_reg
    JUMP label_continue_216276956994
    ...
    ...
    ... 
    ... 
    ...
    JUMP label_216276956994
    label_continue_216276956994:
    ...
    ...
    ...
    ...
    
Two labels are generated marking the start (``label_216276956994:``) and the end of the loop 
(``label_continue_216276956994:``). In loop entry, we always check the current value that the ``dp`` points to and this 
is achieved here via a ``COPYIA`` which on the 2U firmware also affects the zero flag which is tested with that 
``BCRSC``. If that value becomes non-zero, execution jumps at the end of the loop.


Prologue and Epilogue parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to compiling a brainfuck program, we also need to do some housekeeping tasks on entry and exit to a given 
program.

On entry, we need to initialise ``dp`` to the start of the ``tape`` and this would be our "prologue".

And at the end of the program we need to add the declarations for ``dp``, ``tape`` and the indirect ``INCR`` instruction.

In the end, the "skeleton" of a given Brainfuck program always follows the following Digirule ASM structure:

::

    .EQU status_reg=252
    .EQU in_dev=253
    .EQU out_dev=255
    .EQU zero_bit=0
    COPYLR tape dp
    start_program:
    ...
    ...
    ...
    ...
    HALT
    handle_dv_i:
    .DB 0
    dp:
    .DB 0
    RETURN
    tape:
    

And this is it. A Brainfuck compiler by which we can program the Digirule without using a single ASM instruction.




``Hello World`` in Brainfuck
----------------------------

Brainfuck programming deserves a separate section devoted to the way of thinking one needs to adopt to achieve 
secific objectives. While that section is in development, it would still be worth to show here a minimal 
and absolutely simple example of asking the user for two numbers, producing the sum and returning it on the display.

Here is the program:

::

    ,>,[-<+>]<.


And here is what it does:

#. ``,`` Ask user for input, put the value in the current ``dp``
#. ``>`` Increase ``dp``, moving to the next cell
#. ``,`` Ask user for input, put the value in the current ``dp``
#. ``[`` If the current cell (the second cell in the tape) is zero go to step 10
#. ``-`` Subtract 1
#. ``<`` Move to the first cell
#. ``+`` Add one
#. ``>`` Move to the second cell
#. ``]`` Go to step 4
#. ``<`` Move to the first cell
#. ``.`` Output the value to the data leds
#. Stop

And here is what that listing compiles down to:

.. literalinclude:: ../../dg_asm_examples/brainfuck/add_two_nums.dsf
    :language: DigiruleASM
    :linenos:

.. Conclusion
.. ----------
