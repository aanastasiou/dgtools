Brainfuck
=========

This section describes a brainfuck compiler that produces an almost one-to-one mapping between brainfuck 
commands and their implementation in Digirule 2U ASM code. 

If you simply want to know how to compile brainfuck programs using dgtools, you can jump straight to 
:ref:`compile_bf_dgtools`.

For a brief overview of brainfuck's commands, see section :ref:`bf_lang`.

The rest of the sections outline the basic machine that the language targets and how the compiler adapts it to the 
Digirule 2U hardware. 

Brain what?...and why?
----------------------

Brainfuck is a Turing complete language with just 8 commands that operate on a rudimentary "machine" with 
memory, a basic input / output and two very, very (**very**) fundamental mathematical operations. 

Stating that a "machine" is `Turing complete <https://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis>`_ 
implies that *anything that is computable*, can be computed with it. And, stating that this "machine" can achieve this 
with just 8 commands and some memory implies that computation, *any computation*, can be broken down into a minimal 
set of fundamental operations. 

In other words, taken to the extreme, it **is** possible to write a Brainfuck program that implements 
something like an `iterative approximation to finding the square root of a number <https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method>`_, 
or something like `"World of Warcraft" <https://en.wikipedia.org/wiki/World_of_Warcraft>`_. 

It is not going to be easy. It is not going to be human readable or easy to debug and follow (for reasons that are about 
to become obvious)

But it **is**.provably.doable.

Brainfuck was conceived by `Urban Dominic Muller <https://www.youtube.com/watch?v=gjm9irBs96U&feature=youtu.be&t=8722>`_ 
in the early 90s while he was the administrator of `Aminet <http://wiki.aminet.net/index.php/The_history_of_Aminet>`_, 
the largest software repository of Amiga sofware in the world. Muller was inspired by an earlier language 
(`FALSE <http://progopedia.com/language/false/>`_) and both that one and Brainfuck had the same key objective: 
To be compiled to a functioning program with as small a compiler as it is possible.

Perhaps these reasons already make Brainfuck worth a second look, even as yet another demo over some resource 
constrained computer.

But, there is also an impressive little thing happening right here. 

If brainfuck is enough to write **any** program and it is possible for an instruction set to express a 
brainfuck program, then we can use brainfuck's "model" to do away with the intricacies and details of the ASM 
instruction set itself and program the hardware straight in brainfuck...to carry out **any** computation.

Since brainfuck assumes that it runs on a system with some basic facilities (Memory, Input/Output, Arithmetic unit), 
then brainfuck **BECOMES** a sort-of Assembly language for that system [1]_.

And with this, the objective was set: *"Is it possible to write a brainfuck compiler for the Digirule?"*

Needless to say, if you have reached this point, that it **is** possible. And given the proliferation of computer 
languages, compilers, transpilers, etc, it is not even a "new" idea.

It is however fun to have done and if you are interested in finding out more about its inner workings keep reading. 

Alternatively, you can simply jump to the practical section that outlines the Brainfuck programs you can use with 
the brainfuck compiler.



The brainfuck "system"
----------------------

Brainfuck, as a language, is associated with an underlying machine that is very close, in form, 
to `the Turing Machine <https://en.wikipedia.org/wiki/Universal_Turing_machine>`_.

The layout of this "machine" explains directly the instruction set.


The machine
^^^^^^^^^^^

Brainfuck targets a "machine" that is composed of the following peripherals:

1. A "tape", which is an ancient word for "memory" or "an array of numbers"
2. A "Data Pointer" (DP) that points to some point on the tape. 
    * This is quite simply the index within the array 
      of numbers. 
3. An Arithmetic Logic Unit (ALU) 
    * That can only add and subtract...**by one**
4. An input device; and 
5. An output device.


.. _bf_lang:

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

Bear with me here however, because we will soon be writing brainfuck programs that execute on the Digirule.


From brainfuck to Digirule ASM
------------------------------

Implementing the machine
^^^^^^^^^^^^^^^^^^^^^^^^

A brainfuck memory "tape" is quite simply an array. An array in Digirule Assembly can be represented by a base memory 
address (the start of the array) and an offset to a particular memory cell. Let's call this array...``tape``. 

If you would like to catch up with representing arrays in ASM and Digirule ASM in particular, you might want to see 
:ref:`this first <array_indexing>`

Having defined the array, we also need to define its offset. Notice here that in brainfuck, the offset to the 
memory is the "Data Pointer". So, let's define a "variable" called ``dp``, representing the current position within the 
array.

If you would like to catch up with plain simple operations (such as assignments) in Digirule ASM, you might want to see 
:ref:`this first <assignments>`.

Modelling the input and output devices is also easy. On the Digirule, these can be mapped directly to the "keyboard" 
and data led display "peripherals". Both look like simple data transfers between memory locations.


Transpiling the commands
^^^^^^^^^^^^^^^^^^^^^^^^

With very little overhead, it is possible to map the brainfuck commands to Digirule (**2U**) assembly. This will be 
demonstrated here by walking through the implementation of three commands: 

#. The "Move Right" (``>``)
#. The "Add 1" (``+``); and
#. The "Iteration" (``[ ]``).

The first two, produce the same result (increase a "value") but towards different targets. To "move right" 
we simply need to add 1 to the ``dp``. To increase the value that the ``dp`` points at, we need to add one to where it 
points to.

The naive implementation of the first is:

::

    INCR dp
    
However, notice that Brainfuck does not have literals. In plain simple brainfuck, it is impossible to specify ``12`` 
as a value somewhere along the "tape". So, the literal ``12``, in brainfuck is expressed as ``++++++++++++`` which leads 
to adding 12 units to the initial value of the memory tape cell. 

The 
naive implementation therefore, leads to 12 calls to ``INCR`` and more generally :math:`\text{reps} \times 2` 
bytes of memory. Here, :math:`\text{reps}` stands for the number of times the ``+`` symbol appears at a 
specific point in the input program.

For this reason, the brainfuck transpiler, "catches" the repeated application of ``+ - > <`` and converts them to the 
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
``BCRSC``. 

If that value becomes non-zero, execution jumps at the end of the loop.


Prologue and Epilogue parts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to compiling a brainfuck program, we also need to do some housekeeping tasks on entry and exit to a given 
program.

On entry, we need to initialise ``dp`` to the start of the ``tape`` and this would be our "prologue".

And at the end of the program we need to add the declarations for ``dp``, ``tape`` and the indirect ``INCR`` instruction.

In the end, the "skeleton" of a given brainfuck program always follows the following Digirule ASM structure:

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
    

And this is it, a brainfuck compiler by which we can program the Digirule without 
using a single ASM instruction.


.. _compile_bf_dgtools:

Using `dgtools` to compile brainfuck programs
---------------------------------------------

The brainfuck compiler is called :ref:`dgbf <dgbf_desc>` and produces a Digirule Assembly source code file (a `.dsf`) 
that is then compiled to an executable by `dgasm`. ``dgbf`` accepts a single filename and produces output right through 
``stdout``.

Given the brainfuck code in some file ``bf_code.bfc``, a typical command line session goes like this:

::

    \> dgbf.py bf_code.bfc>asm_code.dsf    # Brainfuck --> Assembly
    \> dgasm.py asm_code.dsf -g 2U         # Assembly --> Executable
    \> dgsim.py asm_code.dgb -I            # Simulation
    \> xdg-open asm_code_trace.html        # Output
    

.. note::
    Notice how ``dgsim.py`` was called with ``-I``, putting it in interactive mode. 
    This is necessary only if your program contains I/O commands and you would like to 
    really try entering different numbers yourself. If ``-I`` is not provided, then 
    ``dgsim.py`` will ignore the I/O commands.

For more information on compiling Digirule ASM programs in general, see :ref:`here <intro-topics>`.

Let's try this with a simple program.


``Hello World`` in brainfuck
----------------------------

Brainfuck programming deserves a separate section devoted to the way of thinking one needs to adopt to achieve 
secific objectives. While that section is in development, it would still be worth to show here a minimal 
and absolutely simple example of asking the user for two numbers, producing the sum and returning it on the display.

Here is the program:

::

    ,>,[-<+>]<.


Here is how it works:

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
    
Alternatively, you can skip the whole "user interaction" part and try out a simple ``2+3`` sum with something like:

::

    ++>+++[-<+>]<.


Conclusion
----------

There are a tonne of brainfuck compilers out there. And if you think of a compiler itself as a program, 
there are even Brainfuck interpreters. That is, programs written in brainfuck that 
*accept a brainfuck program and re-produce its result*. 

Modern brainfuck compilers can be created with a size very close to the total memory of a machine such as the Digirule 
(256 bytes) when written in ASM.

But since we have to fit **both** data **and** code in the span of 256 bytes, it was looking as if a compiler that reads 
brainfuck and produces Digirule Assembly was more suitable for this goal.

Writing programs in brainfuck is a really good brain teaser, but, it has an incredibly 
high cost: Speed...and high maintenance...and unreadable code...

It is trivial to show that the speed of execution of adding two numbers depends on the numbers themselves. The higher 
the numbers, the slower the speed that the progam will execute.

Yet, this has not stopped people from using brainfuck to `write anything from interpreters to whole operating 
systems. <https://github.com/search?q=brainfuck>`_. Knowing that it **is** doable is a slippery slope to the tar pit.

For our purposes, brainfuck is a wonderful demonstrator of a basic "model" of computation, one that is based on a linear 
memory segment to carry out any computation.

And from this perspective it is not the only one. 



.. [1] In fact, `this has already been done <https://people.csail.mit.edu/wjun/papers/sigtbd16.pdf>`_
