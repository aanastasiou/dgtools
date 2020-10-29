# The brainfuck compiler

All examples in this folder are compiled and sent to your browser via a Makefile.

Very briefly:

```
  > make html
```

Will compile your code; and

```
  > make clean
```

Will get rid of the intermediate files produced by the compilation process.



To compile some other file (e.g. `exp.bfc` or your own brainfuck source code):

```
  > make BF_SOURCE=exp.bfc html
```

For more details, see following sections.



# Compiling with `Make`

A `Makefile` in this directory orchestrates the compilation process.

The makefile contains two targets:

1. `html`
    * bf_source --> Digirule ASM --> Digirule Binary --> Simulator --> HTML output --> Your browser
    
2. `clean`
    * To delete all intermediate files produced by the `html` rule.
    
If you simply run:

```
  > make html
```

You will see the output of `bf_assign.bfc`.

To change the compilation file, simply call `make` with:

```
  > make BF_SOURCE=<file_name.bfc> html
```

where `<file_name.bfc>` is one of the following files (without the "<..>"):


## Brainfuck examples in this folder


* `add_two_nums.bfc`
    * Asks for two numbers from the user and produces their sum

* `bf_assign.bfc`
    * The Brainfuck way of setting a cell equal to the value of 
      another cell.
    * This is also the default example that will be compiled 
      if you run ``make html`` in this directory

* `exp.bfc`
    * Exponentiation as repeated multiplication
    * Raises 2 to the power of 3
    
* `mul.bfc`
    * Multiplication as repeated addition
    * Multiplies 2 by 5
    
* `setzero.bfc`
    * Iteration / flow control
    * Sets a cell to zero by subtracting while non-zero
    
* `sumnums.bfc`
    * Produces the sum of a sequence of numbers
    
* `swap.bfc`
    * Swaps two numbers in place by a series of assignments.
