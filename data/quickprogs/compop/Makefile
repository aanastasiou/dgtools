compop_lt_trace.html:compop_lt.dgb
	dgsim.py compop_lt.dgb -t 'If (R0 < R1) R2=0xF0 else R2=0x0F' -ts R0 -ts R1 -ts R2

compop_leq_trace.html:compop_leq.dgb
	dgsim.py compop_leq.dgb -t 'If (R0<=R1) R2=0xF0 else R2=0x0F' -ts R0 -ts R1 -ts R2
	
	
compop_lt.dgb:compop_lt.dsf
	dgasm.py compop_lt.dsf

compop_leq.dgb:compop_leq.dsf
	dgasm.py compop_leq.dsf

html: compop_lt_trace.html compop_leq_trace.html
	xdg-open compop_lt_trace.html
	xdg-open compop_leq_trace.html

clean:
	rm *.dgb *.html
