Heads Up Display
================

This is a short note on how to turn your Digirule 2U to an auxiliary little display for up to 2 different parameters.

With this program, the Digirule 2U is used to display up to 2 values simultaneously, right from the command line.

You can use it to display all sorts of things such as your battery charge level, whether you have new email and any 
other "event" you can describe with an integer number from 0 to 255.


What is the display?
--------------------

Every Digirule, from version 2 to 2U is equipped with two rows of LEDs:

1. The upper row, labeled ``A7, A6, A5...A0``, which is normally used to display the current memory address in binary; and
2. The lower row, labeled ``D7, D6, D5...D0``, to display the byte value at the current memory address, also in binary.

When the Digirule powers up, the default behaviour is to have the address LEDs to be showing the current memory address.

It is however possible, to also control them by setting the third bit of the status register to ``1``; and
writing the byte value to depict at address ``254``.

Driving the data LEDs is much more straightforward, by just writing the BYTE value to address 255.

These two rows of LEDs can be used to display a binary number or they can be used as two "bar" displays, depicting a 
bar filling up by depicting the numbers ``1, 3, 7, 15, 31, 63, 127, 254``.

So, the main idea is to write a program that displays the two numbers to the displays and when data becomes available 
on the serial port, it reads it in and goes back to displaying them.

But how do we select the display and send those numbers in?


What are its commands?
----------------------

Our little display is built around a very very simple protocol: ``/<display><number>``. 

``/`` is used as the starting character. This tells the code to read in the next value which here is either a ``0`` or 
``1`` and this corresponds to which bar to set. Send ``/0`` to select the Data LED bar, or ``/1`` to select the 
address LED bar. The final step is to read in the BYTE value which is an integer number from 0 to 255.

So, to set the Data LED bar so that it appears 50% lit (just 4 LEDs being lit), we would send ``/0015`` and similarly,
to send the same value to the Address LED bar we would send ``/1015``.

To simplify things, the BYTE value to be depicted to the LEDs must be 3 digits long. Which means that if you wanted to 
send ``0``, you really have to send ``000``.

This brings about an interesting point about this little demo because to an extend, it is identical to 
:ref:`itoa`.

This is because, we want to be able to send the number to the display in human readable form and this means that it will 
have to be in "ASCII". That is, instead of sending ``A`` (which represents the number 65), we would be sending ``065`` and
this means that before storing the value ``65``, we need to calculate 
:math:`(\text{byte}_0 - 48) \cdot 100 + (\text{byte}_1 - 48) \cdot 10 + (\text{byte}_2 - 48)`.

The reason we are subtracting ``48`` here, is because ``48`` is 
`the ASCII code <https://en.wikipedia.org/wiki/ASCII#Printable_characters>`_ that corresponds to the **symbol** that 
we know as zero.

So, the interpretation of ``065`` simply boils down to evaluating 
:math:`(48 - 48) \cdot 100 + (54 - 48) \cdot 10 + (53 - 48)` prior to storing the 
received value to either the upper or lower display.

Knowing how this is handled now only leaves putting it together with communications...


How to handle the communication?
--------------------------------

The logic for this is very simple. For 99% of its running cycle, the progam reads the two values to depict from memory 
and sends them to the LED displays.

Without communications, this is really straightforward:

.. code-block:: DigiruleASM
    :linenos:
    
    .EQU status_reg=252
    .EQU addr_led_bit=2
    BCLR addr_led_bit status_reg # Enable control of the Address LEDs
    
    display_values:
    COPYRR M1 254
    COPYRR M2 255
    JUMP display_values   # For ever display M1 and M2
    
    M1:
    .DB 32
    M2:
    .DB 16
    
And, when the time comes to update the values, the program needs to jump out of its display loop, check if the received 
message fits the protocol, receive the string, do any necessary conversions and go back to displaying the new values.

It probably reads much more complicated than it really is.

The main loop remains the same, but we now add a ``COMRDY`` to check if a message is being received: 

.. code-block:: DigiruleASM
    :linenos:

    # ...
    # ...
    
    check_input:
    COMRDY
    BCRSS zero_bit status_reg # If data is received COMRDY marks the  
    JUMP load_new_values      # Zero flag and, here, branches out to load_new_values
    display_values:
    COPYRR M1 255
    COPYRR M2 254
    JUMP check_input
    
The next part is simply reading in bytes and converting them to a number:

.. code-block:: DigiruleASM
    :linenos:
    
    # ...
    # ...
    
    load_new_values:
    CBR carry_bit status_reg
    COMIN
    SUBLA 47                    # Is it the / character?
    BCRSS zero_bit status_reg
    JUMP display_values         # If not go back to displaying the values
    CBR carry_bit status_reg
    COMIN
    SUBLA 48
    BCRSC carry_bit status_reg  # Is the display a positive number?
    JUMP display_values
    ADDLA M1
    COPYAR R0
    CBR carry_bit status_reg
    COMIN                       # Receive the first byte...
    SUBLA 48
    COPYAR R1
    COPYLR 100 R2               # Multiply by 100
    MUL R1 R2
    COMIN                       # Receive the second byte...
    SUBLA 48
    COPYAR R2
    COPYRA R1
    COPYLR 10 R1                # Multiply by 10
    MUL R2 R1
    ADDRA R2                    # Add it to the previous product
    COPYAR R2
    COMIN                       # And finally receive the third byte
    SUBLA 48
    ADDRA R2                    # And add it to the previous sum.
    COPYAI R0                   # Now transfer the result to either M1 or M2 
    JUMP display_values         # Get back to the main loop
    

And that is basically it. The only other thing that this code does is deciding whether to send 
the received and converted value to M1 or M2 depending on the bar selection number (the first 
value right after ``/``).

Here is the complete code listing from ``dg_asm_examples/hud/``.

.. literalinclude:: ../../dg_asm_examples/hud/rhud.dsf
    :language: DigiruleASM
    :linenos:


How to communicate with it from another computer?
-------------------------------------------------

Driving the display from another computer is really straightforward and ideally, it involves:

1. Setup the communications port parameters (More importantly speed)
2. Send a message to the communications port.

And all the "complexity" is then due to the way different Operating Systems access the port. 

Here is how to do it on Linux:

If you don't know which "device" your Digirule 2U listens on:

1. Plug the Digirule 2U in
2. Find out which device file corresponds to the serial port
    a. The easiest way to do this is by ``> dmesg|egrep FTDI`` to which your OS will respond with something like
       ``[ 6093.755022] usb 2-2: FTDI USB Serial Device converter now attached to ttyUSB0``. 
    b. From this we know that the serial port the Digirule 2U is connected on is at ``/dev/ttyUSB0``.
3. Make sure that you can write to the serial port
    a. By default, the serial port's access rights might be restricted. But since we know that the only thing that 
       is attached to this serial port is the Digirule 2U, we can go ahead and allow read/write access to it with:
       ``> sudo chmod o+rw /dev/ttyUSB0``.

Once you know which "device" the Digirule 2U uses:

1. Set the communications port parameters
    a. The simplest way to do this is with ``> stty -F /dev/ttyUSB0 9600``
    
2. Send a message to the port
    a. The simplest way to do this is with ``> echo "/0127" > /dev/ttyUSB0``
    

You might think that this is complicated but it is really worth the effort when you consider that on this operating 
system, you can obtain information about every single part of its functionality.

More on this later


Putting it all together
-----------------------

Conclusion
----------
