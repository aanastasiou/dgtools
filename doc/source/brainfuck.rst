A Brainfuck compiler
====================

Brainfuck is probably the most widespread of the "esoteric" programming languages.

It is immensely valuable though, because of two striking characteristics:

1. It is Turing complete.
2. It has 8 "commands", here they are:``+-><.,[]`` and a chunk of memory (e.g a simple array).

Stating that a particular "machine" is Turing complete is...scaringly important. It implies that *anything that is 
computable*, can be computed with this machine. 

Stating that this "machine" can achieve this with just 8 commands and a chunk of memory implies that computation can 
be broken down into a minimal set of fundamental operations. Operations that have nothing to do with CPUs, memory buses
and anyhting else we might already be associating with "computers".

Granted, computers **can** compute stuff. But anything that can add, subtract, iterate and more importantly remember, 
can "compute". In other words, taken to the extreme, it is possible to write a Brainfuck program that implements 
"World of Warcraft". It is not going to be easy. It is not going to be human readable or easy to follow.

But it **is** doable. And this is what makes Brainfuck and other programming languages in the same league, scaringly 
important. And fun, just like a brainteaser.

There are a tonne of Brainfuck compilers out there. And if you think a compiler as a computation process, there are 
even Brainfuck interpreters. That is, programs written in Brainfuck that *operate over an input that represents 
a Brainfuck program and re-produce its outcome*. 

And so the objective was set: *"Is it possible to write a Brainfuck compiler for the Digirule?"*

Because if this is possible, then this means that we can "ignore" the tens of instructions in the Digirule instruction 
set and achieve the same outcome with just 8 Brainfuck instructions.

Needless to say, if you have read up to this point, that it **is** possible. And given the proliferation of computer 
languages, compilers, transpilers, etc, it is not even "new".

It is however fun to have done and if you are interested in finding out more about how it works keep reading. 
Alternatively, you can simply jump to the practical section that outlines the Brainfuck programs you can use with 
the Brainfuck compiler.


The Brainfuck "System"
----------------------

Brainfuck, as a language, is associated with an underlying machine that is very close, in form, to the Turing Machine.
The layout of this "machine" explains directly the instruction set.

The machine
^^^^^^^^^^^

It has a "tape" for memory, a "Data Pointer" (DP) that points to some point on the tape, an Arithmetic Logic Unit (ALU) 
that can only add and subtract **by one**, an input device and an output device.

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

Modelling the machine
^^^^^^^^^^^^^^^^^^^^^

A Brainfuck memory "tape" is quite simply an array. An array in Digirule Assembly can be represented by a base memory 
address (the start of the array) and an offset to a particular memory cell. Let's call this array...``tape``. 

If you would like to catch up with representing arrays in ASM and Digirule ASM in particular, you might want to see 
:ref:`this first <array_indexing>`

Having defined the array, we also need to define its offset. Notice here that in Brainfuck, the offset to the 
memory is the "Data Pointer". So, let's define a "variable" called ``dp``, representing the current position within the 
array.

If you would like to catch up with plain simple operations (such as assignments), you might want to see 
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
we simply need to add 1 to the ``dp``. To increase the value that the dp points at, we need to add one to where it 
points to.

The naive implementation of the first is:

::

    INCR dp
    
However, notice that Brainfuck does not have literals. In plain simple Brainfuck, it is impossible to specify ``12`` 
as the value somewhere along the "tape". So, the literal ``12``, in Brainfuck is ``++++++++++++`` which leads 
to adding 12 units to the initial value of the memory tape cell. The 
naive implementation therefore, leads to 12 calls to ``INCR`` and 24 bytes of memory.

For this reason, the Brainfuck transpiler, "catches" the repeated application of ``+ - > <`` and converts it to the more
efficient:

::

    COPYRA dp
    ADDLA {reps}
    COPYAR dp
    
Where ``{reps}}`` is the number of times the symbol appears in the input. 

This is just 6 bytes in Digirule ASM. The converse command (``<``) has ``SUBLA`` in the place of ``ADDLA``.

Similarly, adding 1 to the value of where the ``dp`` points to, is a matter of
