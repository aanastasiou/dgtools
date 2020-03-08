HALT

problem_data:
.DB 5,0,1,2,3,4

f_pushs:
COPYLA stack
ADDRA stack_ptr
COPYAR f_to
COPYLR r1 f_from
CALL f_copy
INCR stack_ptr
RETURN

f_pops:
COPYLA stack
ADDRA stack_ptr
COPYAR f_from
COPYLR r1 f_to
CALL f_copy
DECR stack_ptr
RETURN

f_copy:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN

stack:
.DB 0,0,0,0,0,0,0,0,0,0
stack_ptr:
.DB 0
r1:
.DB 0
r2:
.DB 0
