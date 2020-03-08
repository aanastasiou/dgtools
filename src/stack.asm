COPYLR 4
CALL f_pushs
COPYLR 2
CALL f_pushs
COPYLR 0
CALL f_pushs
HALT

f_pushs:
COPYLA stack
ADDRA stack_ptr
COPYAR f_to
COPYRR r1 f_from
CALL f_copy
INCR stack_ptr
RETURN

f_pops:
COPYLA stack
ADDRA stack_ptr
COPYAR f_from
COPYRR r1 f_to
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
