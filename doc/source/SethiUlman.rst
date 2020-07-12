Arbitrary Expression Evaluation
===============================


Motivation
----------

Throughout these notes, I have often used the expression "Up here, we can write...", to 
highlight the conceptual difference between high level programs and their low level counterparts
that achieve exactly the same goals.

Evaluating arbitrary mathematical expressions using a constrained CPU is a prime example of this.

*Up here, we can write...", things like ``y = a*x*x*x + b*x*x + c*x + d`` but there is **absolutely NO** 
low level (ASM) instruction available that evaluates expressions such as that one. 

Instead, what is available most of the times is a **limited amount of registers** and a set of elementary instructions 
that implement the equivalents of *assignment, multiplication, division, etc*.

So, clearly, there must be an entirely predictable and deterministic way by which an arbitrary mathematical expression 
can be turned into a handful of "instructions" that lead to its result. But what is it?


Register Allocation Optimisation
--------------------------------

The problem of evaluating an arbitrary mathematical expression under the constraints posed by a given machine, 
is known as the "Register Allocation Optimisation" problem.

It is an incredibly interesting problem that is deeply rooted in Computer Science and complexity theory.

The basic, tractable, solutions were developed very early on, in the evolution of computers and  
