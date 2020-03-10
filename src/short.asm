.EQU led_reg=255

start:
COPYLR 4 r0
CALL f_push
COPYLR 4 r0
CALL f_push
CALL q_add_ab
CALL f_pop
COPYRR r0 led_reg
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


f_jump_by_ref:
.DB 28
f_jump_to_ref:
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
