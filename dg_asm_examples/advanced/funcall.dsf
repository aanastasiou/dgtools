# Demonstrates the use of the stack to perform function calls
# Positional arguments to a function are pushed on to the stack prior to calling the function
# The function reads arguments in (poping them from the stack) and when it is done, pushes the 
# result back on to the stack.
#
# The function that is implemented is `a + b` and the result is also sent to the display.

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
# A very simple function to add two numbers
# This is equivalent to
#
# def q_add_ab(a,b):
#    return a+b
#
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
