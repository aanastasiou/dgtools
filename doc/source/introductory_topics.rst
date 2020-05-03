.. _intro-topics:

Introducing ``dgtools``
=======================

The objective of this introductory section is to demonstrate the key use cases of ``dgtools`` by example.

Digirule 2 ASM knowledge is not essential, but a general knowledge of ASM, even at introductory level, would be 
favourable. This walkthrough is based on the very simple example of adding two numbers which goes through 5 revisions 
here, each one introducing one new feature or capability of `dgtools`. 

Throughout the following section, it is assumed that `dgtools` is installed on a virtualenv, the virtualenv is 
activated and the current working directory is `src/data/intro/`.

Adding two literals
-------------------

Adding two literals is the "Hello World" of Digirule 2 programming. It is a matter of three commands in 
Digirule 2 ASM:

.. code-block:: DigiruleASM
    :linenos:
    :name: simpleadd_1
    
    COPYLA 1
    ADDLA 1
    HALT
    
This listing is available in :download:`data/intro/simpleadd_1.dsf <../../data/intro/simpleadd_1.dsf>`


Copy literal 1 to the accumulator, add literal 1 to the accumulator and stop.
At the end of this program, we expect the accumulator to have the value ``2``.

To verify this using ``dgtools``, run the following (from within the ``src`` directory):

.. code::

    > dgasm.py simpleadd_1.dsf
    > dgsim.py simpleadd_1.dgb


If you now open the generated trace file (``simpleadd_1_trace.html``) via a browser and scroll all the way down to 
the last time step, you can confirm the value that the accumulator holds.


.. _simple_add_with_mem:

Adding two literals saving the result to memory
----------------------------------------------- 

Leaving the result of the addition to the accumulator is fine, but more commonly these results would have to be shifted
out of the Accumulator to memory.

Our new listing is now:

.. code-block:: DigiruleASM
    :linenos:
    :name: simpleadd_2

    COPYRA r0
    ADDRA r1
    COPYAR r3
    HALT
    r0:
    .DB 1
    r1:
    .DB 1
    r3:
    .DB 0
    
This listing is available in :download:`data/intro/simpleadd_2.dsf <../../data/intro/simpleadd_2.dsf>`


Here, there are three labels (``r0, r1, r2``) that simply "tag" three locations in memory that hold initial literal 
values (``1, 1 ,0`` respectively).
These are *hard coded* into the program here. To get a full dump of the memory space at **every** time step 
of execution, we will need to run ``dgsim`` with an extra parameter. The complete workflow is as follows:

.. code::

    > dgasm.py simpleadd_2.dsf
    > dgsim.py simpleadd_2.dgb --with-dump

Compiling and running this program will result in a slightly longer ``_trace.md`` file, but again, scrolling all the 
way to the end and reviewing the memory dump, it should be evident that the label ``r3`` now points to the literal 2.

A more convenient way to monitor specifically the value of ``r3`` is to tell ``dgsim`` to focus on it. This also 
involves the use of ``dginspect`` as follows:

1. Compile the program: 
    * ``> dgasm.py simpleadd_2.dsf``
2. Use ``dginspect`` to obtain all defined symbols and their addresses:
    * ``> dginspect.py simpleadd_2.dgb``
3. Run ``dgsim`` telling it to "track" ``r3``:
    * ``> dgsim.py simpleadd_2.dgb -ts r3``

Adding multiple ``-ts`` options, keeps adding named references for ``dgsim`` to track. For example, suppose we wanted 
to track all three memory locations, then step 3 would become: 

``> dgsim.py simpleadd_2.dgb -ts r0 -ts r1 -ts r3``

For an example of the sort of output produced by ``dgsim``, you can see 
`this file <_static/simpleadd_2_trace.html>`_.

Adding two literals, sending the output to the Data LEDs
--------------------------------------------------------

Certain registers of the Digirule 2 are memory mapped. For example, the Data LEDs are accessible at address 255.
``dgasm`` allows the definition of "symbols" that resolve to specific expressions. At the moment, "symbols" are used to
define numeric constants, but in the future, these symbols might expand to whole expressions, akin to C's macros. 

Defining constants in this way does not take up any memory space. When the assembler comes across a "symbol" defined in 
this way, it simply substitutes its value.

The code now is:

.. code-block:: DigiruleASM
    :linenos:
    :name: simpleadd_3

    .EQU led_register=0xFF
    COPYLA a
    ADDLA b
    COPYAR r3
    COPYAR led_register
    HALT
    r3:
    .DB 0

This listing is available in :download:`data/intro/simpleadd_3.dsf <../../data/intro/simpleadd_3.dsf>`

This program can be tried out in one of the ways that were explained previously. 

.. note::
    It would be useful to note here the difference between a "Label" and a "Symbol". The **value** of a label is the 
    address it points to in memory. The **value** of a symbol is the literal that was assigned to it through the 
    ``.EQU`` directive.

If we now run ``dginspect`` with ``> dginspect.py simpleadd_3.dgb`` we can see at its output two 
separate sections of offsets, the "Label" and "Static Symbol". Both of these show offsets within the program memory 
where **a label points to** and where **a literal value would be substituted at**.

Since this program now produces some sort of output we can try to "key it in" to the Digirule 2. To make this process 
easier, ``dginspect`` includes the ``-b`` option that "dumps" the complete assembled memory region as pairs of 
``ADDR:VALUE`` values *formatted in binary*. To key the program in, just make sure that a given memory address on 
the Digirule2 (indicated by the A0-7 LEDs) maps to the corresponding ``VALUE`` (indicated by the D0-7 LEDs).

To see what this looks like:

.. code::

    > dginspect.py simpleadd_3.dgb -b
    
This will simply dump everything to ``stdout``, which means that it can be stored to be reviewed later with:

.. code::

    > dginspect.py simpleadd_3.dgb -b>add3_bin_output.txt
    
Or, if you are in Linux, simply send it to `less <https://en.wikipedia.org/wiki/Less_(Unix)>`_ with:

.. code::

    > dginspect.py simpleadd_3.dgb|less

In either case, the binary dump for ``simpleadd_3.dgb`` would look like this:

.. code::
    
        ADDR:VALUE   
    00000000:00000100
    00000001:00000001
    00000010:00001000
    00000011:00000001
    00000100:00000101
    00000101:00001001
    00000110:00000101
    00000111:11111111
    00001000:00000000
    00001001:00000000
    00001010:00000000
    00001011:00000000
    ...
    ...
    ...
    ...
    ...



Adding a literal and a user supplied input
------------------------------------------

The Digirule 2 has an elementary input device, a keyboard, attached to the CPU at address ``253``. Reading that 
"register" allows the program to read user input in the form of a binary number. 

The Digirule 2 Virtual Machine includes a flexible mechanism that is called *interactive mode* that allows the 
simulation to take user input into account. This is specified to ``dgsim`` with option ``-I``.

The code listing for this example is as follows:

.. code-block:: DigiruleASM
    :linenos:
    :name: simpleadd_4

    .EQU a=1
    COPYLA a
    ADDRA 253
    COPYAR r3
    HALT
    r3:
    .DB 0

This listing is available in :download:`data/intro/simpleadd_4.dsf <../../data/intro/simpleadd_4.dsf>`

The compilation process is the same as previously, but since this program attempts to read from address `253`, 
we might want to try the code over real user input. To achieve this, we modify the call to `dgsim` as follows:


.. code::

    > dgasm.py simpleadd_4.dsf
    > dgsim.py simpleadd_4.dgb -I

This time around, once the CPU tries to read from ``253``, the user will be prompted to provide a **binary** input 
(i.e `0b00000010`) which the program then adds 1 to and stores to the memory location labeled ``r3``.

Again, the result of the final state can be inspected through ``dginspect``.


.. _cplx_intro_example_5:

Adding two literals with command line parametrisation
-----------------------------------------------------

It probably has become apparent by now that ``dgsim`` can operate as a separate virtualised computing unit. It can 
run programs and save its final state and it also provides ways of extracting those values from its memory space.

In fact, it is possible to *parametrise* Digirule 2 programs, call them and then extract values from the final memory 
space as follows:

.. code-block:: DigiruleASM
    :linenos:
    :name: simpleadd_5

    COPYRA a
    ADDRA b
    COPYAR r3
    HALT

    r3:
    .DB 0

    a:
    .DB 2
    b:
    .DB 6

This listing is available in :download:`data/intro/simpleadd_5.dsf <../../data/intro/simpleadd_5.dsf>`

This program specifies 1 byte ``a,b`` which hold literals that participate in addition and ``r3`` that 
points to a one byte memory location that receives the result of the addition.

Very briefly, ``a,b`` will become the **parameters** (two numbers that can be reset **without recompiling the program**) 
and ``r3`` will be the memory location that holds the final result.

The complete workflow is as follows, notice here *which .dgb file is inspected for the results of the calculation*:

1. Compile the program
    * ``> dgasm.py simpleadd_5.dsf``
2. Run the program
    * ``> dgsim.py simpleadd_5.dgb``
3. Inspect the result as stored in `r3`
    * ``> dginspect.py simpleadd_5_memdump.dgb -g r3`` 
    * With the program in its original form, this value should be ``8``.
4. **Change parameter a to 3**
    * ``> dginspect.py simpleadd_5.dgb -s 8 3``
    * Don't worry about overwriting ``simpleadd_5.dgb``, its original form is still maintained in a ``.bak`` file.
    * Notice here that `8` is the offset of variable `a`
5. Run the program again
    * ``> dgsim.py simpleadd_5.dgb``
6. Inspect the final result now
    * ``> dginspect.py simpleadd_5_memdump.dgb -g r3`` 
    * With the parameters given here, this value should be ``9``
    
7. Start keying the final result in with:
    * ``> dginspect.py simpleadd_5_memdump.dgb -b``
    

This is probably the most involved workflow using ``dgtools`` to take full control of program execution.

Each one of the three tools has more capabilities that were not expanded upon here but can be reviewed with ``--help``.
For more information please see section :ref:`detailed_script_descriptions`.

With these points in mind, it is now time to move to :ref:`advanced topics <advanced-topics>` demonstrating more 
complex code on the Digirule 2.
