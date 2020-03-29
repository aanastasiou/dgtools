.. _pov_light_stick:

POV Light Stick
===============

POV stands for `Persistence of Vision <https://en.wikipedia.org/wiki/Persistence_of_vision>`_ and it is the reason why 
we perceive fast changing snapshots as moving images. A Light Stick is...exactly what it describes, a stick with a 
set of lights attached to it.  But putting the two together means that by carefully timing which lights turn on and 
off, it is possible to "paint" images, whether on slow human eyes or long exposure photographs such as `this 
one <https://www.kickstarter.com/projects/700404819/trickstick>`_.

Since the Digirule has 16 LEDs and is stick-like, it was inevitable not to try to turn it into a POV light stick. 

This section outlines the simplest, un-optimised program that implements a light stick on the Digirule 2. Yes, it is 
possible to optimise the code further but for the moment we are aiming for the simplest straightforward option.

The reason this example is in the more "advanced" programs section is because it is using the indirect copy version of
``COPYRR``, the details of which can be found in section :ref:`advanced-topics`.

The main idea
-------------

POV displays are extremely simple. They usually involve storing the "image" as a bitmap in memory which is progressively
scanned and its data used to turn the stick's LEDs on and off.

At their simplest form, POV displays simply scan the bitmap at a fixed rate, based on practical experiments of what 
seems to look right. At their most complex forms, light sticks synchronise the scanning of the bitmap to the movement 
of the stick so that no matter how fast or slow, forwards or backwards, faster or slower it moves, the bitmap will 
display exactly as intended. In addition, the more complex POV light sticks might add bitmap upload functionality, 
storing multiple bitmaps, displaying rolling image sequences and others.

For the Digirule2 POV light stick, we take the simplest approach (for the moment):

#. Define a bitmap in memory.
#. Fetch a line from memory, turn the LEDs on
#. Wait for at least :math:`\frac{1}{10}` of a second, for the pixels to register in the brain.
#. Turn the LEDs off
#. Wait for the same time
#. Repeat from step 2 until all bitmap lines have been read. Once you run out lines, simply start from the beginning.


Defining the bitmap
------------------- 

The "bitmap" can be defined as a set of 8 bytes but since ``dgasm`` understands binary number literal values, defining 
that memory area in the editor also provides a sort of preview for it. 

Here for example is the letter ``A``:

.. code::

    pov_data:
    .DB 0b00111100
    .DB 0b01000010
    .DB 0b10000001
    .DB 0b11111111
    .DB 0b10000001
    .DB 0b10000001
    .DB 0b10000001
    .DB 0b10000001
    pov_data_len:
    .DB 8
    
This is part of :download:`../../data/advanced/pov.asm`

There is no reason for this bitmap to strictly be an 8x8 bitmap but to let the code know of its length we also define 
the variable ``pov_data_len`` with a static value of 8, for this bitmap.


Scanning the bitmap
-------------------

Probably the easiest thing to do: Set a counter to the start of the bitmap memory region and advance it by one 
to fetch the next line. This is a very common "pattern" when dealing with "arrays" (to the extent an array data type 
can be defined within the Digirule's capabilities) and proceeds like this:

.. code::

    reset:
    COPYLR pov_data pov_counter

``pov_data`` is a label and ``dgasm.py`` will "translate" it to its literal value. By executing this ``COPYLR``, the 
content of variable ``pov_counter`` at the start of the program now points to the beginning of ``pov_data``.


Wasting time
------------

Steps 3 and 5, from our extremely simple routine outline earlier, include a very small delay. Delays are painfully 
simple for CPUs and are based on a very simple trick: Let the CPU do nothing else but count down from a large number.

On the Digirule2 there are two ways to control the speed of execution of a program:

#. Use the ``SPEED`` command (which controls the speed that a program is executed globally).
#. Use one or more counters to keep the CPU busy.

Since the second way of introducing delays depends on how large a number the CPU can count down from and that the 
most straightforward counter is 1 byte long, both ways of controlling the speed will be used here. The Digirule might 
not be the fastest CPU but it will count down from 255 incredibly fast.

The delay routine is as simmple as:

.. code::

    delay:
    COPYLR delay_count r1
    delay_loop:
    NOP
    NOP
    NOP
    NOP
    DECRJZ r1
    JUMP delay_loop
    RETURN


This is part of :download:`../../data/advanced/pov.asm`


Putting it all together
-----------------------

There is really not much else to this program, except a few cosmetic additions with a few ``.EQU`` definitions to change
constants without having to recompile the program.

The main loop for the light stick is available below:


.. code::

    CBR 2 status_reg
    COPYLR led_reg f_to
    reset:
    COPYLR pov_data pov_counter
    COPYRR pov_data_len r0
    start:
    COPYRR pov_counter f_from
    CALL f_copy
    CALL delay
    COPYLR 0 led_reg
    CALL delay
    INCR pov_counter
    DECRJZ r0
    JUMP start
    JUMP reset

    f_copy:
    .DB 7
    f_from:
    .DB 0
    f_to:
    .DB 0
    RETURN

    delay:
    COPYLR delay_count r1
    delay_loop:
    DECRJZ r1
    JUMP delay_loop
    RETURN
    pov_data:
    .DB 0b00111100
    .DB 0b01000010
    .DB 0b10000001
    .DB 0b11111111
    .DB 0b10000001
    .DB 0b10000001
    .DB 0b10000001
    .DB 0b10000001
    pov_data_len:
    .DB 8
    pov_counter:
    .DB 0
    r0:
    .DB 0
    r1:
    .DB 0

This is part of :download:`../../data/advanced/pov.asm`


One thing to notice here is that whenever a variable was required it was simply allocated. It is however possible to 
write a more optimised version of this code that uses less memory. However, even at this sloppy level the program 
ends up being very very small, leaving as much memory free as possible for......user defined bitmaps.


Conclusion
----------

This example, shows a way of "drawing" images using one row of LEDs on the Digirule2. However, the "output device", 
the "screen", of the Digirule2 has two rows of 8 pixels.

Therefore, it would be possible to reduce the flickering rate by display two rows at the time or even create a 
"scrolling image" through a "window" that is just 2x7 wide. 
