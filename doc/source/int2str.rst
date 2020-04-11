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
individual bytes as 1 number. That is, the number 939 (`0b 0000 0011 | 1010 1011`) would only be "perceived" as 
`0x03, 0xAB`. The point of the conversion here is to go from `0x03, 0xAB` to `939`. 
 
Coincidentally, the key mathematical operation behind converting an integer from its binary 
representation to a **human readable** (decimal) representation, is *division*, which, the Digirule2 does not have an 
operation for.

Let's give Digirule these routines...


Outline of the conversion
-------------------------

Converting an integer to its string representation is not different than trying to *print the bits that compose it*.


Integer division
----------------

Putting it all together
-----------------------

Conclusion
----------


`itoa`
------

"Integer To Ascii" (`itoa`) is what the function would be called 
https://en.wikibooks.org/wiki/C_Programming/stdlib.h/itoa
