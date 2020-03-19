# Some thoughts on Digirule's instruction set

## `SUBLA` and `ADDLA`

It is not necessary to have both because `SUBLA` can be expressed via `ADD*A` (either `L` or `R`) via complement-2 
addition.

**But**, this consumes memory.

Where now we can do:

```
COPYLA 4
SUBLA 2
HALT
```

We would have to do:

```
COPYLA 2
XORLA 0xFF
ADDLA 1
ADDLA 4
HALT
```

To achieve the complement-2 we need 2 more bytes than the existing instruction set.

This is great, from the point of view of instruction set and memory economy.


# Control flow via `JUMP` and `ADDRPC`

Again, `ADDRPC` can be simulated with a "template" JUMP "by reference" command. For example:

```
f_jump:
.DB 28
f_jump_addr:
.DB 0
```

Obviously that RETURN there will never be reached and it should be removed (it occupies one extra byte).

Here, calculate the jump address, move it to `f_jump_addr` and `JUMP f_jump`.

The "problem" with simulating these opcodes is the extra work that is required to copy the reference and `JUMP` to the 
"template" function.

So, one possible modification to the instruction set would be to add commands that do something **by reference**. 

For example, `COPYRR` **by reference** and `JUMP` **by reference**.

We need a CLC command to clear carry so that SHIFTRR and SHIFTRL can behave simply as shifts
