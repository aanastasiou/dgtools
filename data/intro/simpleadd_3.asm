# Implements the addition of two constants.
# This is equivalent to the statement `r3 = a + b` where `a` and `b` have been defined earlier
# as constants.
# Havin performed the addition, the result is also sent to the display.
 
.EQU led_register=0xFF
.EQU a=1
.EQU b=1

COPYLA a
ADDLA b
COPYAR r3
COPYAR led_register
HALT
r3:
.DB 0

