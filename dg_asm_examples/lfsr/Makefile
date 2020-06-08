lfsr_9bit_trace.html: lfsr_9bit.dgb
	dgsim.py lfsr_9bit.dgb -t "9 bit LFSR Random Number Generator" -ts array:10 -mn 400

lfsr_trace.html: lfsr.dgb
	dgsim.py lfsr.dgb -t "LFSR Random Number Generator" -ts array:10 -mn 400
	
lfsr.dgb:lfsr.dsf
	dgasm.py lfsr.dsf

lfsr_9bit.dgb:lfsr_9bit.dsf
	dgasm.py lfsr_9bit.dsf
	
html: lfsr_trace.html lfsr_9bit_trace.html
	xdg-open lfsr_trace.html
	xdg-open lfsr_9bit_trace.html

clean:
	rm *.dgb *.html
