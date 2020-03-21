.EQU rnd_state=128
start:
COPYRA state
COPYRR state r1
SHIFTRR state
CBR 1 252
SHIFTRR state
CBR 1 252
XORRA state
SHIFTRR state
CBR 1 252
XORRA state
SHIFTRR state
CBR 1 252
XORRA state
ANDLA 1
COPYAR r2
SHIFTRR r1
CBR 1 252
DECRJZ r2
JUMP set_bit
clr_bit:
SBR 7 r1
JUMP resume
set_bit:
CBR 7 r1
resume:
COPYRR r1 state
DECRJZ r0
JUMP start
HALT
state:
.DB rnd_state
r0:
.DB 10
r1:
.DB 0
r2:
.DB 0
