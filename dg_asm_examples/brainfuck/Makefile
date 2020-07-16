bf_code.dsf:bf_code.bfc
	cat bf_code.bfc|./brainfuck_to_asm.py ->bf_code.dsf
	
bf_code.dgb:bf_code.dsf
	dgasm.py bf_code.dsf -g 2U
	
bf_code_trace.html:bf_code.dgb
	dgsim.py bf_code.dgb --with-dump -mn 1500 -I -ts dp -ts tape:4
	
html:bf_code_trace.html
	xdg-open bf_code_trace.html
