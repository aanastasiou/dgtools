# Advanced Digirule 2 programming

`dgtools` provides an assembler that understands labels and this makes it possible to start creating more involved 
programs. 

However, one thing the Digirule does not specify is a stack which is an important part of function calling.

This section first establishes a stack, then a stack and a set of registers and then based on these pre-requisites it 
demonstrates function calling with parameters passed on the stack.

## Defining a stack

The Digirule 2 is capable of referencing approximately 256 bytes of main memory. Therefore, it should be possible to 
implement a stack as a statically allocated array of `N` values where the push and pop operations are carried out 
at the "head" of the stack.

The only problem here is that the Digirule 2 does not have an opcode for reading memory **by reference**. The command 
`COPYRR` copies memory **content** from one address to another address but (out of the box) it cannot copy memory from 
where an address is pointing to, to where another address is pointing to. 

### Adding "Copy By Reference" functionality
To achieve this, we are going to use the assembler's label capabilities to "build" a `COPYRR` that copies by reference.
This is achieved by writing a "template" function:

```
f_copy_by_ref:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN
```

*This is part of `data/advanced/stack.asm`*

The first byte (`7`) is the opcode of `COPYRR`, the second byte is labeled `f_from` and the third byte is labeld `f_to`.

The CPU is "tricked" into thinking that it executes a `COPYRR` but this is now a parametrisable `COPYRR` that copies
between two **computable** addresses.

To copy between two references, **calculate** the references (if required), move the references to addresses `f_from` 
and `f_to` and then execute a `CALL f_copy_byref`. The CPU will fetch the `7`, decide it is a `COPYRR`, read in the 
next two bytes, perform the copy, hit the RETURN and go back to where it was called from.


### Getting the head of the stack

Defining the stack through `dgasm` is as trivial as defining a label and immediately populating it with values. For 
example:

```
stack:
.DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F
``` 

There is no particular reason for the default values other than making this memory range stand out in a memory dump.

The stack also needs a way of pointing to its head address. This can be achieved by using another "labeled" location:

```
stack_ptr:
.DB 0
```

Having defined the stack, now we need to define its two fundamental operations: `push, pop`. This is relatively easy, 
all we have to do is find out where the head is pointing to and send (or retrieve) a number to (or from) that location.
This is achieved with:

```
f_push:
CALL f_get_stack_head
COPYAR f_to
COPYLR r0 f_from
CALL f_copy_by_ref
INCR stack_ptr
RETURN

f_pop:
DECR stack_ptr
CALL f_get_stack_head
COPYAR f_from
COPYLR r0 f_to
CALL f_copy_by_ref
RETURN

f_get_stack_head:
COPYLA stack
ADDRA stack_ptr
RETURN
```

*This is part of `data/advanced/stack.asm`*


**NOTE:** This is a bit of a roundabout way of doing it because it assumes that the stack head location has to 
be re-calculated prior to every push or pop. An alternative way of doing it is to estalibsh `f_get_stack_head` as 
`f_init_stack` and then use `stack_ptr` directly at subsequent calls.

But for these examples, we will simply take the scenic route, as it makes the traces more interesting too.

All that `f_push, f_pop` do is to calculate where the head of the stack is and then pass that address as either the 
`f_from` or `f_to` "parameter" of the `COPYRR` by reference.

**But**, how are these "low level" functions going to communicate with the rest of the code? The Digirule 2 does not 
specify a standardised register set.

By now, it should be clear that this is not a problem at all because we can use the labeled `.DB` capabilities of the 
assembler, to specify the equivalent of a "register" or even a complete set of registers.

For the purposes of this example, register `r0` is used as the intermediate register for the `f_push, f_pop` functions.

This example pushes values `0,1,2,3,2,1,0,1,2` to the stack. The complete listing is as follows:
```
start:
COPYLR 0 r0
CALL f_push
COPYLR 1 r0
CALL f_push
COPYLR 2 r0
CALL f_push
COPYLR 3 r0
CALL f_push
COPYLR 2 r0
CALL f_push
COPYLR 1 r0
CALL f_push
COPYLR 0 r0
CALL f_push
COPYLR 1 r0
CALL f_push
COPYLR 2 r0
CALL f_push
HALT

f_push:
CALL f_get_stack_head
COPYAR f_to
COPYLR r0 f_from
CALL f_copy_by_ref
INCR stack_ptr
RETURN

f_pop:
DECR stack_ptr
CALL f_get_stack_head
COPYAR f_from
COPYLR r0 f_to
CALL f_copy_by_ref
RETURN

f_get_stack_head:
COPYLA stack
ADDRA stack_ptr
RETURN

f_copy_by_ref:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN


r0:
.DB 0

stack_ptr:
.DB 0
stack:
.DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F
```

*This is `data/advanced/stack.asm`*


## Using the stack to implement parameter passing to function calls

Now that the Digirule 2 has a stack, it can call any function it likes with any number of parameters it likes by 
adopting a ['calling convention'](https://en.wikipedia.org/wiki/Calling_convention) and defining a standardised 
set of registers.

In this section, the addition of two numbers is packaged in a two parameter function as follows:

```
q_add_ab:
CALL f_pop
COPYRR r0 t0
CALL f_pop
COPYRR r0 t1
COPYRA t0
ADDRA t1
COPYAR r0
CALL f_push
RETURN
```

*This is part of `data/advanced/funcall.asm`*

Here, `q_add_ab` first pops the numbers from the stack to "temporary registers", performs the addition, pushes the 
result back on to the stack and returns. All that the caller has to do now is to pop the stack on the "other side of 
the call" to retrieve the result.

The complete listing is now:

```
.EQU a=1
.EQU b=2

start:
COPYLR a r0
CALL f_push
COPYLR b r0
CALL f_push
CALL q_add_ab
CALL f_pop
COPYRR r0 255
HALT

q_add_ab:
CALL f_pop
COPYRR r0 t0
CALL f_pop
COPYRR r0 t1
COPYRA t0
ADDRA t1
COPYAR r0
CALL f_push
RETURN

f_push:
CALL f_get_stack_head
COPYAR f_to
COPYLR r0 f_from
CALL f_copy_by_ref
INCR stack_ptr
RETURN

f_pop:
DECR stack_ptr
CALL f_get_stack_head
COPYAR f_from
COPYLR r0 f_to
CALL f_copy_by_ref
RETURN

f_get_stack_head:
COPYLA stack
ADDRA stack_ptr
RETURN

f_copy_by_ref:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN


r0:
.DB 0
r1:
.DB 0
r2:
.DB 0
r3:
.DB 0
r4:
.DB 0
r5:
.DB 0
r6:
.DB 0
r7:
.DB 0

t0:
.DB 0
t1:
.DB 0
t2:
.DB 0
t3:
.DB 0
t4:
.DB 0
t5:
.DB 0
t6:
.DB 0
t7:
.DB 0

stack_ptr:
.DB 0
stack:
.DB 0xF0,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0x0F
```
*This is `data/advanced/stack.asm`*


# Conclusion

Now that Digirule 2 has a stack and a set of standardised registers, it is possible to start thinking about implementing 
a higher level language that compiles down to its assembly.

It should then be possible to write arbitrarily complex programs to carry out functionality possibly not envisaged for
the Digirule 2.

But, aside from being 8bit and having a very limited amount of memory, **there is nothing that can be expressed with a 
[stack machine](https://en.wikipedia.org/wiki/Stack_machine) that Digirule cannot do**.

It might be slow and somewhat difficult to define, but Digirule will eventally compute it.
