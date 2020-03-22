.EQU status_reg=252
.EQU data_led=255
.EQU rnd_state=42
.EQU gen_n_numbers=10
COPYLR array array_idx
start:
BCRSS 0 state
JUMP op_a_was_0
JUMP op_a_was_1
op_a_was_0:
BCRSS 5 state
JUMP op_a_was_0_op_b_was_0
JUMP op_a_was_0_op_b_was_1
op_a_was_1:
BCRSS 5 state
JUMP op_a_was_1_op_b_was_0
JUMP op_a_was_1_op_b_was_1
op_a_was_1_op_b_was_1:
op_a_was_0_op_b_was_0:
CBR 1 status_reg
JUMP continue
op_a_was_0_op_b_was_1:
op_a_was_1_op_b_was_0:
SBR 1 status_reg
continue:
SHIFTRR state
COPYLR state f_from
COPYRR array_idx f_to
CALL f_copy
INCR array_idx 
DECRJZ r0
JUMP start
HALT
state:
.DB rnd_state
r0:
.DB gen_n_numbers

f_copy:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN

array:
.DB 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
array_idx:
.DB 0
