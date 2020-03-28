# Demonstrates the definition and use of a simple stack, set of registers and using
# the stack to perform function calls.

# Main program entry point
start:
COPYLR 0 r0 # General purpose register r0 is used as the argument to f_push
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
# Pushes `r0` to the top of the stack
CALL f_get_stack_head
COPYAR f_to
COPYLR r0 f_from
CALL f_copy_by_ref
INCR stack_ptr
RETURN

f_pop:
# Pops the top of the stack on to `r0`
DECR stack_ptr
CALL f_get_stack_head
COPYAR f_from
COPYLR r0 f_to
CALL f_copy_by_ref
RETURN

f_get_stack_head:
# Returns the address of the stack head.
COPYLA stack
ADDRA stack_ptr
RETURN

f_copy_by_ref:
# Performs an indirect copy between the addresses pointed to by `f_from, f_to`.
# This also shows a "template" function. It is constructed and parametrised in 
# memory prior to being called from the main program.

.DB 7   # COPYRR opcode
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
