.EQU status_reg=252
.EQU rnd_state=42
.EQU gen_n_numbers=10
COPYLR array array_idx
start:
COPYRA state
COPYRR state r1
SHIFTRR state
CBR 1 status_reg
SHIFTRR state
XORRA state
CBR 1 status_reg
SHIFTRR state
XORRA state
CBR 1 status_reg
SHIFTRR state
XORRA state
ANDLA 1
COPYAR r2
CBR 1 status_reg
SHIFTRR r1
DECRJZ r2
JUMP clr_bit
set_bit:
SBR 7 r1
JUMP resume
clr_bit:
CBR 7 r1
resume:
COPYRR r1 state
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
r1:
.DB 0
r2:
.DB 0

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
