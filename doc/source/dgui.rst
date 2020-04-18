Compiling via ``dgui.py``
=========================

``dgtools`` is composed of three simple programs that work together to compile, simulate and inspect 
software for the Digirule.

To make these more user friendly, ``dgtools`` incorporates a text based graphical user interface that gathers 
input from the user and orchestrates the rest of the build process. A screenshot of that is available in 
the following figure:

.. figure:: figures/fig_dgui_ss.png

    The ``dgui.py`` script invoked on ``simpleadd_1.dsf`` through a relative path.
    
The ``dgui.py`` can be invoked at any point in the filesystem and only requires that the ``.dsf`` file that is 
passed at its input is an existing Digirule Source File.

Once the parameters are set to the desired values, use the arrow keys to select ``<OK>``, click enter and see 
output for any messages on the compilation process either from ``dgasm.py`` or ``dgsim.py``.

The ``dgui.py`` can also be invoked through the ``DigiruleASM`` build environment within the Sublime text editor.
