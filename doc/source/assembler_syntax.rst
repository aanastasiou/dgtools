Assembler Syntax
================

``dgasm.py``, the ``dgtools`` assember understands three types of "input":

1. Assembler Directives
    * Commands that target the assembler and do not necessarily lead to 
      producing Digirule 2 ASM code in the final binary.
      
2. Digirule2 Assembly commands
    * Plain Digirule2 Assembly
    
3. Comments

Please note that, at the moment, the reserved keywords of both the assembler directives and assembly commands 
**must be typed in uppercase**.


Assembler Directives
--------------------

Assembler directives always start with a dot. At the moment, the following directives are supported:


.EQU
^^^^

Assigns an expression to a "symbol". At the moment, the expression can only be a numeric literal. For example:

.. code:: DigiruleASM

    .EQU a=5
    
Here the symbol is ``a`` and the expression is ``5``.

All that the assembler does when it encounters a "symbol" is to substitute it with its "expression".

``.EQU`` definitions can also be used to parametrise a program and study its behaviour when it is executed with 
different inputs. This is demonstrated clearly in section :ref:`intro-topics`

.DB
^^^

Sets the default value of one or more ``BYTE`` size memory location(s).

This assembler directive, along with the ability to define Labels (next section) make it possible for ``dgasm`` to 
understand variables and memory pointers.

``.DB`` has two forms, the simplest being:

.. code:: DigiruleASM

    .DB 0
    
This tells the assembler to emmit a plain ``0`` at the current memory offset. Multiple sequential ``.DB`` directives 
cause sequential addresses in memory to be set to ``BYTE`` (always) values as in:

.. code:: DigiruleASM

    .DB 0
    .DB 0b11110000
    .DB 0x0F
    
But this can also be expressed in one single line as :

.. code:: DigiruleASM

    .DB 0, 0b11110000, 0x0F
    
The directive also understands double quoted strings and "unrolls" them to their individual character values. For 
example:

.. code:: DigiruleASM

    .DB 'ABC', 10, 13, "DEF"
    
This will be unrolled to the equivalent ``65,66,67,10,13,68,69,70``, automatically. 
    
If a ``.DB`` is not preceded by the definition of a label, it is very difficult to address the memory it points to.
To do that, continue reading on "Labels".


Labels
^^^^^^

Labels are defined by an identifier, terminated by a colon (``:``). Labels are not translated to ASM directly, but they
cause the assembler to "note" the memory offset where a label was defined in a table of symbols, similar to the one 
established by ``.EQU`` directives (but separate).

When the assembler encounters a label as a parameter of a command, it substitutes its symbol for the memory address 
it points to. This is incredibly useful in two situations:

1. Branching commands (e.g. ``JUMP``)
2. Memory offsets as targets to memory copy commands

The branching use case is the most straightforward, consider the following example:

.. code:: DigiruleASM

    start:
    NOP
    NOP
    NOP
    JUMP start

This will effectively trap the CPU into repeated cycles of ``NOP`` operations. 

In this case, when the assembler first encounters ``start``, it notes down its memory offset and when it encounters 
it again as the argument to ``JUMP`` it substitutes it for whatever offset it points to.

The use of labels as targets to memory copy commands is similar but more interesting. Consider the following snippet 
for example:

.. code:: DigiruleASM

    COPYLR 1 r0
    r0:
    .DB 0

Here, ``r0`` is used as a "target" for ``COPYLR`` and it will substitute ``r0`` for the memory offset where a plain 
``0`` has been reserved through the use of a ``.DB`` directive.

For more illustrative examples of ``.DB``, see section :ref:`advanced-topics`

Digirule 2 Instruction Set
--------------------------

.. note::

    The current version of ``dgtools`` supports the latest model too (Digirule 2U) but the instruction set 
    will be adjusted to the final after its release.
    
    

The Assembly language that Digirule 2 executes is detailed in the PDF user manual that accompanies the hardware 
and is also available `here <https://bradsprojects.com/wp-content/uploads/Digirule2-User-Manual.pdf>`_.

An overview of the instruction set is provided here with the instructions grouped according to function:

+--------------+--------------+--------------+--------------+--------------+
| Flow Control |    Memory    |  Arithmetic  |     Logic    |     Other    |
+==============+==============+==============+==============+==============+
| HALT         | COPYLR       | ADDLA        | ANDLA        | NOP          |
+--------------+--------------+--------------+--------------+--------------+
| DECRJZ       | COPYLA       | ADDRA        | ANDRA        | SPEED        |
+--------------+--------------+--------------+--------------+--------------+
| INCRJZ       | COPYAR       | SUBLA        | ORLA         |              |
+--------------+--------------+--------------+--------------+--------------+
| BCRSC        | COPYRA       | SUBRA        | ORRA         |              |
+--------------+--------------+--------------+--------------+--------------+
| BCRSS        | COPYRR       | SHIFTRL      | XORLA        |              |
+--------------+--------------+--------------+--------------+--------------+
| JUMP         | CBR          | SHIFTRR      | XORRA        |              |
+--------------+--------------+--------------+--------------+--------------+
| CALL         | SBR          | DECR         |              |              |
+--------------+--------------+--------------+--------------+--------------+
| RETLA        |              | INCR         |              |              |
+--------------+--------------+--------------+--------------+--------------+
| RETURN       |              |              |              |              |
+--------------+--------------+--------------+--------------+--------------+

* ``HALT, RETURN, NOP`` are 1 Byte instructions.
* ``COPYLR, COPYRR, BCRSC, BCRSS`` are 3 byte instructions.
* All other instructions are 2 byte instructions.

In addition, ``dgasm`` will substitute constants and labels with their content if they were to be used as arguments 
in these instructions.

For example, the following two snippets are equivalent:

.. code:: DigiruleASM

    COPYLA 1
    

.. code:: DigiruleASM

    .EQU a=1
    
    COPYLA a
    

Comments
--------

Any sequence of characters preceded by a hash symbol (``#``) is completely and utterly ignored by the assembler.

Comments can appear at the beginning of a line:

.. code:: DigiruleASM

    # And in this way it is also possible to define
    # comments that expand to more than one lines
    
Or, they can appear inline with code:

.. code:: DigiruleASM

    COPYLA 1 # Copies the literal 1 to the Accumulator and also shows here the use of an inline comment.
    

Comments, although parsed, are not processed at all by ``dgasm``. 

Comments are there for the use of humans, not machines. Comment frequently and write for comprehension not out of 
obligation.
