assign1_trace.html:assign1.dgb
	dgsim.py assign1.dgb --with-dump -t 'Literal assignment' -ts R0
	
assign2_trace.html:assign2.dgb
	dgsim.py assign2.dgb --with-dump -t 'Assigning to expression 1' -ts R0 -ts R1

assign3_trace.html:assign3.dgb
	dgsim.py assign3.dgb --with-dump -t 'Assigning to expression 2' -ts R0 -ts R1

assign1.dgb: assign1.dsf
	dgasm.py assign1.dsf
	
assign2.dgb: assign2.dsf
	dgasm.py assign2.dsf
	
assign3.dgb: assign3.dsf
	dgasm.py assign3.dsf

clean:
	rm *.dgb *.html

show:assign1_trace.html assign2_trace.html assign3_trace.html
	xdg-open assign1_trace.html &
	xdg-open assign2_trace.html & 
	xdg-open assign3_trace.html &
