.EQU led_register=0xFF
COPYLA a
ADDLA b
COPYAR r3
COPYAR led_register
HALT
r3:
.DB 0

