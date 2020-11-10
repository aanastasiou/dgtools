# Brainfuck Programs

To compile and simulate the programs in this directory, type the following on your terminal:

```
    > make clean;make BF_CODE=<full name of Super Stack source file from below> html
```

If you simply do a:

```
    > make html;
```

you will compile and simulate the DEFAULT selection from below.


* `add_two_nums.bfc`
    * Asks for two numbers from the user and produces their sum

* `assign.bfc` (DEFAULT)
    * Brainfuck's "special" way of handling assignment.
    * This is also the default example that will be compiled 
      if you run ``make html`` in this directory
      
* `setzero.bfc`
    * The shortest (real) "program" in Brainfuck.
    * Setting a cell to zero is equivalent to decreasing its value until it hits zero.
    
* `swap.bfc`
    * Swap two numbers in memory

* `multiply.bfc`
    * Multiplication as repeated addition 
    
* `expon.bfc`
    * Exponentiation (a.k.a raising to the power of) as repeated multiplication
    
* `sequence.bfc`
    * Setting up a numerical sequence in memory
    
* `sumnums.bfc`
    * Summing a sequence of numbers
    
    
* `bf_code.bfc`
    * Contains the `bf_equals.bfc` example. This is the default 
      Brainfuck source code file which `dgtools` uses to produce 
      the Assembly, binary, hex and trace HTML from. See also
      `Makefile`.
