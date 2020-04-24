.. _long_counter:

Longest counter possible
========================

How high could a Digirule2 count, if a Digirule2 could count high?

The answer is:

.. code::

    13179894006841322479854620122170084926912013522466037943
    43706666106002621345561402409288057184803891421955702295
    37632116730115317754316483048406036918009001764045349509
    06937942664422915800236844171640278724942888243990142286
    01614308240494248737033497020218523643351874839672280540
    71617415464737987072935096400220358078369415051687589577
    07318893133586444139557373748585033528908823852943154899
    46453488394423398674401553548965414666791756989103381598
    43390356075193849158904064883576072848642143122338502025
    09552412952006441842894260164101947268276461637650779996
    16
    
...or 2 raised to the power of 233 **bytes** (1864 bits).

Here is how and why...


What does a counter do?
-----------------------

Counting is a very basic step in mathematical thinking and the most elementary 
"sequential logic" circuit.

In positional numeral systems, the digits of a number represent a "count" of powers
of the numeral system's basis.

Decimal counters (where the basis is 10) count ones (:math:`1 \cdot 10^0`), 
tens (:math:`1 \cdot 10^1`), hundreds (:math:`1 \cdot 10^2`), thousands (:math:`1 \cdot 10^3`), 
tens of thousands (:math:`1 \cdot 10^4`), hundreds of thousands (:math:`1 \cdot 10^5`), 
millions (:math:`1 \cdot 10^6`),... and so on.

Similarly, binary counters (where the basis is 2) count ones (:math:`1 \cdot 2^0`), doubles (:math:`1 \cdot 2^1`), 
quadroubles (:math:`1 \cdot 2^2`), double quadroubles (:math:`1 \cdot 2^3`)...and so on.

In this way the number :math:`1492_{10} = 1 \cdot 10^3 + 4 \cdot 10^2 + 9 \cdot 10^1 + 2 \cdot 10^0` but in the 
binary system  :math:`1492_{2} = 1\cdot 2^{10} + 0 \cdot 2^9 + 1 \cdot 2^8+ 1 \cdot 2^7 + 1 \cdot 2^6 + 0 \cdot 2^5 + 1 \cdot 2^4 + 0 \cdot 2^3 + 1 \cdot 2^2 + 0 \cdot 2^1 + 0 \cdot 2^0`

Binary counters of :math:`n` flip-flops can count up to :math:`2^n` before resetting themselves and counting again 
from 0. In our example, a counter of 10 bits, can count from 0 to 2048 and thus *can contain* the number 1492.

Electronic circuits that implement counters are composed of :math:`n` flip-flops connected in series that get toggled
by a "clock" signal.


How does the Digirule2 counts?
-----------------------------

CPUs contain counters in the form of registers and include commands (such as ``INC,DEC``) to increase or
decrease the value of a register by one. They also contain extra "flags" for special events such as 
the counter becoming zero.



A momentous occassion
---------------------

Conclusion
----------
