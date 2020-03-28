# Implements a very simple random number generator 
# using a 9bit LFSR. The one extra bit is coming from the 
# carry flag on the Digirule2, because its `SHIFTRR, SHIFTRL` 
# commands perform shift THROUGH the carry.

# To make this random number generator re-usable, we would have 
# to store the carry bit as well between calls, consuming two 
# bytes of memory.

.EQU status_reg=252      # Status register on the Digirule2
.EQU data_led=255        # LED register
.EQU rnd_state=42        # Initial state for the random number generator
.EQU gen_n_numbers=10    # How many numbers to generate
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
