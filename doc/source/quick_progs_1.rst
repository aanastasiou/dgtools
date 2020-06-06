.. _qfs_1:

Quickfire snippets :: Volume 1
==============================

Tiny Digirule ASM riffs.


``Hello World``
---------------

.. raw:: html
    
    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">&quot;Hello World&quot;, this is the shortest <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a> ASM demo program. You can key it in by entering the numbers 4,1,8,1,0, or you can dgasm and dgsim it first. See <a href="https://t.co/poHGOWZ4Si">https://t.co/poHGOWZ4Si</a> for more. What can you do in 256 bytes of code? <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a> <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> <a href="https://t.co/ttCnye60db">pic.twitter.com/ttCnye60db</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1264437480494899202?ref_src=twsrc%5Etfw">May 24, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


.. literalinclude:: ../../data/quickprogs/hellosum/hellosum.dsf
    :language: DigiruleASM
    :linenos:
    
The Quick Brown Fox Jumps Over The Lazy Dog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">&quot;The quick brown fox jumps over the lazy dog&quot; is a pangram phrase where every letter of English is used exactly once. Here is a <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a> equivalent, in <a href="https://twitter.com/hashtag/DigiruleASM?src=hash&amp;ref_src=twsrc%5Etfw">#DigiruleASM</a>, where every operation is used exactly once. All figures produced via <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a>: <a href="https://t.co/poHGOWZ4Si">https://t.co/poHGOWZ4Si</a> <a href="https://t.co/pzWxQdq03K">pic.twitter.com/pzWxQdq03K</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1264799368986660864?ref_src=twsrc%5Etfw">May 25, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

.. literalinclude:: ../../data/quickprogs/qbfjold/qbfjold.dsf
    :language: DigiruleASM
    :linenos:

    

Assignments
-----------

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Most <a href="https://twitter.com/hashtag/programming?src=hash&amp;ref_src=twsrc%5Etfw">#programming</a> languages have assignments. But, just typing a=42 in an editor, is not enough. Something must realise the intention. Here is what assignments come down to on the <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a>. All figures via: <a href="https://t.co/oD2DmHWhbB">https://t.co/oD2DmHWhbB</a> <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a> <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> <a href="https://t.co/GUX87mgX8t">pic.twitter.com/GUX87mgX8t</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1264944312422477824?ref_src=twsrc%5Etfw">May 25, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


Assigning a literal
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/assignments/assign1.dsf
    :language: DigiruleASM
    :linenos:
    

Assigning to expression
^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/assignments/assign2.dsf
    :language: DigiruleASM
    :linenos:
    

Assigning to expression with indirect addressing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/assignments/assign3.dsf
    :language: DigiruleASM
    :linenos:



Swapping the values of two variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">You can just &quot;swap two variables&quot;, or you can use &quot;Parallel Assignment&quot;. On the <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a>, it is a matter of 3 or 15 clock ticks. All figures by <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> (<a href="https://t.co/oD2DmHWhbB">https://t.co/oD2DmHWhbB</a>) <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a><br><br>Remember which algorithm uses so many swaps that it gets all...fizzy? <a href="https://t.co/z7Bqrmin3S">pic.twitter.com/z7Bqrmin3S</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1265334382950256646?ref_src=twsrc%5Etfw">May 26, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

.. literalinclude:: ../../data/quickprogs/simpleswap/swap_simple.dsf
    :language: DigiruleASM
    :linenos:
    
    
.. literalinclude:: ../../data/quickprogs/simpleswap/swap_indirect.dsf
    :language: DigiruleASM
    :linenos:
    

Array Indexing
--------------

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Up here, we can write my_array[5] but this implies not one but two operations: discover the address, fetch from address. Here is how arrays are expressed on the <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a>. All figures via <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> (<a href="https://t.co/oD2DmIdS39">https://t.co/oD2DmIdS39</a>) <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a> <a href="https://t.co/2FA2JRmNb3">pic.twitter.com/2FA2JRmNb3</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1265681671451316224?ref_src=twsrc%5Etfw">May 27, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


.. literalinclude:: ../../data/quickprogs/arrayindexing/arrayindexing.dsf
    :language: DigiruleASM
    :linenos:


Conditional branching & the ``if`` command
------------------------------------------

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">When you write &quot;if (R0&lt;R1) {} else {}&quot;, how is it evaluated by a CPU? What does an IF look like when it comes to actually &quot;doing it&quot;?<br> <br>Here it is, on a <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a>, simplest form of branching. <br><br>All figures using <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> (<a href="https://t.co/oD2DmIdS39">https://t.co/oD2DmIdS39</a>) <a href="https://twitter.com/hashtag/RetroComputing?src=hash&amp;ref_src=twsrc%5Etfw">#RetroComputing</a> <a href="https://t.co/WQnjrny0GD">pic.twitter.com/WQnjrny0GD</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1266044059329552384?ref_src=twsrc%5Etfw">May 28, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


.. literalinclude:: ../../data/quickprogs/compop/compop_lt.dsf
    :language: DigiruleASM
    :linenos:
    

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">There is a difference between &quot;if (R0&lt;R1)...&quot; and &quot;If (R0&lt;=R1)...&quot; and on the <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a> that difference is 2 clock cycles. <br><br>EVERY symbol counts. <br><br>What can you do with 256 _bytes of code_?<br><br>All figures via <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> (<a href="https://t.co/oD2DmHWhbB">https://t.co/oD2DmHWhbB</a>) <a href="https://twitter.com/hashtag/retrocomputing?src=hash&amp;ref_src=twsrc%5Etfw">#retrocomputing</a> <a href="https://t.co/fRDH8KRRkO">pic.twitter.com/fRDH8KRRkO</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1266066708902612993?ref_src=twsrc%5Etfw">May 28, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

.. literalinclude:: ../../data/quickprogs/compop/compop_leq.dsf
    :language: DigiruleASM
    :linenos:
    

Iteration
---------

.. raw:: html

    <blockquote class="twitter-tweet"><p lang="en" dir="ltr">Yesterday was &quot;Conditional Branching&quot; day in <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a> land. <br>Diverting execution depending on an expression soon leads to doing things repeatedly until a condition is met.<br>FOR and WHILE ASM code on a <a href="https://twitter.com/hashtag/Digirule?src=hash&amp;ref_src=twsrc%5Etfw">#Digirule</a>.<br><br>All figures via <a href="https://twitter.com/hashtag/dgtools?src=hash&amp;ref_src=twsrc%5Etfw">#dgtools</a> (<a href="https://t.co/oD2DmIdS39">https://t.co/oD2DmIdS39</a>) <a href="https://twitter.com/hashtag/RetroComputing?src=hash&amp;ref_src=twsrc%5Etfw">#RetroComputing</a> <a href="https://t.co/dk4uGPEZ2r">pic.twitter.com/dk4uGPEZ2r</a></p>&mdash; AthanasiosAnastasiou (@athanastasiou) <a href="https://twitter.com/athanastasiou/status/1266406448487002113?ref_src=twsrc%5Etfw">May 29, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>


.. literalinclude:: ../../data/quickprogs/forloop/forloop.dsf
    :language: DigiruleASM
    :linenos:



    

Copy a memory block
^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/copymemblock/copymemblock.dsf
    :language: DigiruleASM
    :linenos:
    

Swap values between two memory blocks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../../data/quickprogs/swapmemblock/swapmemblock.dsf
    :language: DigiruleASM
    :linenos:



Find minimum num in an array
----------------------------

Here is how ASM pieces together a for-loop: It's a counter followed by a numeric comparison.

.. literalinclude:: ../../data/quickprogs/findmin/findmin.dsf
    :language: DigiruleASM
    :linenos:
    

Sort an array
-------------

.. literalinclude:: ../../data/quickprogs/simplesort/selectsort.dsf
    :language: DigiruleASM
    :linenos:
    
    
    
Onwards, to :ref:`Volume 2 <qfs_2>`.


