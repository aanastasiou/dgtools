# Implements a very simple Persistence of Vision (POV) light stick 
# in the Digirule2
 
.EQU status_reg=252    # Status register on the Digirule2
.EQU led_reg=255       # Display register
.EQU delay_count=255   # Time between LED flashes   
.EQU speed_setting=55  # Speed setting for the whole CPU
SPEED speed_setting
CBR 2 status_reg
COPYLR led_reg f_to
reset:
COPYLR pov_data pov_counter
COPYRR pov_data_len r0
start:
COPYRR pov_counter f_from
CALL f_copy
CALL delay
COPYLR 0 led_reg
CALL delay
INCR pov_counter
DECRJZ r0
JUMP start
JUMP reset

f_copy:
.DB 7
f_from:
.DB 0
f_to:
.DB 0
RETURN

delay:
COPYLR delay_count r1
delay_loop:
DECRJZ r1
JUMP delay_loop
RETURN
pov_data:
.DB 0b00111100
.DB 0b01000010
.DB 0b10000001
.DB 0b11111111
.DB 0b10000001
.DB 0b10000001
.DB 0b10000001
.DB 0b10000001
pov_data_len:
.DB 8
pov_counter:
.DB 0
r0:
.DB 0
r1:
.DB 0
