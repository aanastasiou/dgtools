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
